from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

from core.database import PyObjectId


class FrameworkBase(BaseModel):
    name: str
    language: str
    purpose: str
    scaling_poss: bool
    db_integration: bool
    licence_type: str

    class Config:
        json_encoders = {
            ObjectId: str
        }


class FrameworkCreate(FrameworkBase):
    pass


class FrameworkUpdate(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    purpose: Optional[str] = None
    scaling_poss: Optional[bool] = None
    db_integration: Optional[bool] = None
    licence_type: Optional[str] = None


class FrameworkInDB(FrameworkBase):
    id: PyObjectId = Field(
        alias="_id",
    )
