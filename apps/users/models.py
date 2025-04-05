from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

from core.database import PyObjectId


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_expert: bool = False

    class Config:
        json_encoders = {
            ObjectId: str
        }


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str
