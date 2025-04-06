from core.database import PyObjectId
from .models import LibraryBase


class LibraryResponse(LibraryBase):
    id: PyObjectId

    class Config:
        from_attributes = True
