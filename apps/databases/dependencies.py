from fastapi import Depends, HTTPException, status
from bson.errors import InvalidId

from .services import get_database


async def get_valid_database(database_id: str):
    try:
        database = await get_database(database_id)
        if not database:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Database not found"
            )
        return database
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid database ID format"
        )
