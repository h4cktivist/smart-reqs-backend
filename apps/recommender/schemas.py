from pydantic import BaseModel, Field

from core.database import PyObjectId


class ResultResponse(BaseModel):
    id: PyObjectId = Field(
        alias="_id",
    )
    request_id: PyObjectId
    framework_ids: list[PyObjectId]
    library_ids: list[PyObjectId]
    db_ids: list[PyObjectId]

    class Config:
        from_attributes = True
