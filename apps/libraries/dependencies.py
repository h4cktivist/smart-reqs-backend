from fastapi import HTTPException, status
from bson.errors import InvalidId

from .services import get_library


async def get_valid_library(library_id: str):
    try:
        lib = await get_library(library_id)
        if not lib:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Library not found"
            )
        return lib
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid library ID format"
        )
