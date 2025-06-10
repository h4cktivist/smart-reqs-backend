from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from apps.recommender.models import RequestInDB
from apps.users.dependencies import get_current_user
from apps.users.models import UserInDB
from .services import get_unanswered_requests, answer_request
from .schemas import ExpertResponse


router = APIRouter(prefix='/api/expert', tags=['expert'])


@router.get('/unanswered', response_model=List[RequestInDB])
async def get_unanswered(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_expert:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return await get_unanswered_requests()


@router.post('/answer/{request_id}')
async def answer_unanswered_request(
        request_id: str,
        expert_response: ExpertResponse,
        current_user: UserInDB = Depends(get_current_user)
):
    if not current_user.is_expert:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return await answer_request(request_id, expert_response)
