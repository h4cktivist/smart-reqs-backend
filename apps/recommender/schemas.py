from typing import Optional
from pydantic import BaseModel, Field

from core.database import PyObjectId


class ResultResponse(BaseModel):
    id: PyObjectId = Field(
        alias="_id",
    )
    request_id: PyObjectId
    frameworks: list[str]
    libraries: list[str]
    databases: list[str]

    class Config:
        from_attributes = True
