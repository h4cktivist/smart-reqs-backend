from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator
from bson import ObjectId


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


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    is_expert: Optional[bool] = None

    @model_validator(mode='after')
    def check_passwords(self):
        if self.new_password and not self.current_password:
            raise ValueError("Current password is required to change password")
        return self


class UserInDB(UserBase):
    hashed_password: str
