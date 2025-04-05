from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, services, dependencies
from .models import DatabaseCreate, DatabaseUpdate

from apps.users.dependencies import get_current_user
from apps.users.models import UserInDB

router = APIRouter(prefix="/api/databases", tags=["databases"])


@router.post("/", response_model=schemas.DatabaseResponse)
async def create_database(
    database: DatabaseCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can create databases"
        )
    return await services.create_database(database)


@router.get("/", response_model=list[schemas.DatabaseResponse])
async def read_databases():
    return await services.get_all_databases()


@router.get("/{database_id}", response_model=schemas.DatabaseResponse)
async def read_database(database: schemas.DatabaseResponse = Depends(dependencies.get_valid_database)):
    return database


@router.put("/{database_id}", response_model=schemas.DatabaseResponse)
async def update_database(
    database_id: str,
    database: DatabaseUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can update databases"
        )
    updated_db = await services.update_database(database_id, database)
    if not updated_db:
        raise HTTPException(status_code=404, detail="Database not found")
    return updated_db


@router.delete("/{database_id}")
async def delete_database(
    database_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can delete databases"
        )
    if not await services.delete_database(database_id):
        raise HTTPException(status_code=404, detail="Database not found")
    return {"message": "Database deleted successfully"}
