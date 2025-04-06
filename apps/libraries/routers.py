from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, services, dependencies
from .models import LibraryCreate, LibraryUpdate

from apps.users.dependencies import get_current_user
from apps.users.models import UserInDB

router = APIRouter(prefix="/api/libraries", tags=["libraries"])


@router.post("/", response_model=schemas.LibraryResponse)
async def create_library(
    library: LibraryCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can create librarys"
        )
    return await services.create_library(library)


@router.get("/", response_model=list[schemas.LibraryResponse])
async def read_librarys():
    return await services.get_all_libraries()


@router.get("/{library_id}", response_model=schemas.LibraryResponse)
async def read_library(library: schemas.LibraryResponse = Depends(dependencies.get_valid_library)):
    return library


@router.put("/{library_id}", response_model=schemas.LibraryResponse)
async def update_library(
    library_id: str,
    library: LibraryUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can update librarys"
        )
    updated_lib = await services.update_library(library_id, library)
    if not updated_lib:
        raise HTTPException(status_code=404, detail="Library not found")
    return updated_lib


@router.delete("/{library_id}")
async def delete_library(
    library_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can delete librarys"
        )
    if not await services.delete_library(library_id):
        raise HTTPException(status_code=404, detail="Database not found")
    return {"message": "Library deleted successfully"}
