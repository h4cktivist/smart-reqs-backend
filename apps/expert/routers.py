from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from apps.recommender.models import RequestInDB
from apps.users.dependencies import get_current_user
from apps.users.models import UserInDB
from .services import get_unanswered_requests


router = APIRouter(prefix='/api/expert', tags=['expert'])


@router.get('/unanswered', response_model=List[RequestInDB])
async def get_unanswered(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_expert:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return await get_unanswered_requests()
