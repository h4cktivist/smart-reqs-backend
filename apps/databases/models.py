from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class DatabaseBase(BaseModel):
    name: str
    db_type: str
    scaling_poss: bool
    big_data_poss: bool
    acid_support: bool
    licence_type: str


class DatabaseCreate(DatabaseBase):
    pass


class DatabaseUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    scaling_poss: Optional[bool] = None
    big_data_poss: Optional[bool] = None
    acid_support: Optional[bool] = None
    licence_type: Optional[str] = None


class DatabaseInDB(DatabaseBase):
    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
