from fastapi import HTTPException, status
from bson.errors import InvalidId

from .services import get_framework


async def get_valid_framework(framework_id: str):
    try:
        framework = await get_framework(framework_id)
        if not framework:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Framework not found"
            )
        return framework
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
