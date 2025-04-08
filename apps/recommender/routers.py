from fastapi import APIRouter, Depends, HTTPException, status

from apps.users.dependencies import get_current_user
from apps.users.models import UserInDB

from . import schemas, services
from .models import RequestCreate, RequestInDB


router = APIRouter(prefix="/api/recommender", tags=["recommender"])


@router.post("/", response_model=RequestInDB)
async def get_request(
        request: RequestCreate,
        current_user: UserInDB = Depends(get_current_user)
):
    return await services.get_request(request, current_user)
