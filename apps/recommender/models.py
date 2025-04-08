from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

from core.database import PyObjectId


class RequestBase(BaseModel):
    user_id: PyObjectId
    title: str
    idea_description: str
    functional_reqs: str
    product_type: str
    db_needed: bool
    big_data_needed: bool
    data_structure: str
    data_analysis_needed: bool
    ml_needed: bool
    languages_preferences: Optional[list[str]] = []
    licensing_type: str
    scaling_needed: bool
    autotesting_needed: bool
    datetime: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }


class RequestCreate(BaseModel):
    title: str
    idea_description: str
    functional_reqs: str
    product_type: Optional[str] = None
    db_needed: Optional[bool] = None
    big_data_needed: Optional[bool] = None
    data_structure: Optional[str] = None
    data_analysis_needed: Optional[bool] = None
    ml_needed: Optional[bool] = None
    languages_preferences: Optional[list[str]] = []
    licensing_type: Optional[str] = None
    scaling_needed: Optional[bool] = None
    autotesting_needed: Optional[bool] = None


class RequestInDB(RequestBase):
    id: PyObjectId = Field(
        alias="_id",
    )

    class Config:
        json_encoders = {PyObjectId: str}
        arbitrary_types_allowed = True
