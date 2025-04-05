from core.database import PyObjectId
from .models import FrameworkBase


class FrameworkResponse(FrameworkBase):
    id: PyObjectId
    
    class Config:
        from_attributes = True
