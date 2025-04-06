from typing import Optional

from bson import ObjectId
from fastapi import HTTPException, status

from core.database import get_user_collection
from core.security import get_password_hash, verify_password
from .models import UserCreate, UserInDB, UserUpdate
from .schemas import UserResponse


async def create_user(user: UserCreate) -> UserInDB:
    user_collection = get_user_collection()

    if await user_collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = get_password_hash(user.password)
    user_db = UserInDB(
        **user.dict(exclude={"password"}),
        hashed_password=hashed_password,
    )

    result = await user_collection.insert_one(user_db.dict(by_alias=True))
    new_user = await user_collection.find_one({"_id": result.inserted_id})
    return new_user


async def get_user(email: str) -> Optional[UserResponse]:
    user_collection = get_user_collection()
    user = await user_collection.find_one({"email": email})
    return UserResponse(**user) if user else None


async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user_collection = get_user_collection()
    user = await user_collection.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user['hashed_password']):
        return None
    return user


async def update_user(user_id: str, update_data: UserUpdate, current_user: UserResponse) -> UserResponse:
    collection = get_user_collection()
    update_dict = {}

    if str(current_user.id) != user_id and not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    sensitive_fields = ['email', 'username', 'new_password']
    if any(getattr(update_data, field) is not None for field in sensitive_fields):
        if not update_data.current_password or not verify_password(update_data.current_password,
                                                                   current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )

    if update_data.username is not None:
        if await collection.find_one({"username": update_data.username, "_id": {"$ne": ObjectId(user_id)}}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        update_dict["username"] = update_data.username

    if update_data.email is not None:
        if await collection.find_one({"email": update_data.email, "_id": {"$ne": ObjectId(user_id)}}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        update_dict["email"] = update_data.email

    if update_data.new_password is not None:
        update_dict["hashed_password"] = get_password_hash(update_data.new_password)

    if update_data.is_expert is not None and current_user.is_expert:
        update_dict["is_expert"] = update_data.is_expert

    if not update_dict:
        return UserResponse(**current_user.dict())

    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_dict}
    )

    if result.modified_count == 1:
        updated_user = await collection.find_one({"_id": ObjectId(user_id)})
        return UserResponse(**updated_user)

    return UserResponse(**current_user.dict())
