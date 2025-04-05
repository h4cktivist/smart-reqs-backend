from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, services, dependencies
from .models import FrameworkCreate, FrameworkUpdate

from apps.users.dependencies import get_current_user
from apps.users.models import UserInDB


router = APIRouter(prefix="/api/frameworks", tags=["frameworks"])


@router.post("/", response_model=schemas.FrameworkResponse)
async def create_framework(
    framework: FrameworkCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can create frameworks"
        )
    return await services.create_framework(framework)


@router.get("/", response_model=list[schemas.FrameworkResponse])
async def read_frameworks():
    return await services.get_all_frameworks()


@router.get("/{framework_id}", response_model=schemas.FrameworkResponse)
async def read_framework(framework: schemas.FrameworkResponse = Depends(dependencies.get_valid_framework)):
    return framework


@router.put("/{framework_id}", response_model=schemas.FrameworkResponse)
async def update_framework(
    framework_id: str,
    framework: FrameworkUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can update frameworks"
        )
    updated_fr = await services.update_framework(framework_id, framework)
    if not updated_fr:
        raise HTTPException(status_code=404, detail="Framework not found")
    return updated_fr


@router.delete("/{framework_id}")
async def delete_framework(
    framework_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only experts can delete frameworks"
        )
    if not await services.delete_framework(framework_id):
        raise HTTPException(status_code=404, detail="Framework not found")
    return {"message": "Framework deleted successfully"}
