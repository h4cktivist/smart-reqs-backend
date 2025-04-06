from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from core.database import PyObjectId


class LibraryBase(BaseModel):
    name: str
    language: str
    purpose: str
    licence_type: str

    class Config:
        json_encoders = {
            ObjectId: str
        }


class LibraryCreate(LibraryBase):
    pass


class LibraryUpdate(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    purpose: Optional[str] = None
    licence_type: Optional[str] = None


class LibraryInDB(LibraryBase):
    id: PyObjectId = Field(
        alias="_id",
    )

    class Config:
        json_encoders = {PyObjectId: str}
        arbitrary_types_allowed = True
