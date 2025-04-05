from pydantic import Field
from bson import ObjectId

from .models import DatabaseBase


class DatabaseResponse(DatabaseBase):
    id: str = Field(
        alias="_id",
        default_factory=lambda: str(ObjectId()),
    )

    class Config:
        from_attributes = True
