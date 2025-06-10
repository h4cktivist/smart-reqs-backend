from typing import Optional
from pydantic import BaseModel

class ExpertResponse(BaseModel):
    frameworks: Optional[list[str]] = None
    libraries: Optional[list[str]] = None
    databases: Optional[list[str]] = None
    min_devs: Optional[int] = None
    max_devs: Optional[int] = None