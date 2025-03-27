from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, model_field) -> dict:
        return {"type": "string", "format": "uuid"}


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
