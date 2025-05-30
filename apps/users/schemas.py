from pydantic import BaseModel, Field

from apps.users.models import UserBase
from core.database import PyObjectId


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    username: str


class UserResponse(UserBase):
    id: PyObjectId = Field(
        alias="_id",
    )
    hashed_password: str

    class Config:
        from_attributes = True


class UserLoginRequest(BaseModel):
    email: str
    password: str
