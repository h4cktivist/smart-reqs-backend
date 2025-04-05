from typing import Optional
from fastapi import HTTPException, status

from core.database import get_user_collection
from core.security import get_password_hash, verify_password
from .models import UserCreate, UserInDB
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
