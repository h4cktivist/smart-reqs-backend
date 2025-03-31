from bson import ObjectId
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: str = Field(
        alias="_id",
        default_factory=lambda: str(ObjectId()),
    )
    username: str
    email: str
    is_expert: bool


class UserLoginRequest(BaseModel):
    email: str
    password: str
