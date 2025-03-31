from pydantic import BaseModel, EmailStr
from bson import ObjectId


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_expert: bool = False


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
