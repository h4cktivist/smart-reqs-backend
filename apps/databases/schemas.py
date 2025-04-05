from core.database import PyObjectId
from .models import DatabaseBase


class DatabaseResponse(DatabaseBase):
    id: PyObjectId
    class Config:
        from_attributes = True
