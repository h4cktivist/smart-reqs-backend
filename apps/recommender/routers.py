from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from apps.users.dependencies import get_current_user
from apps.users.models import UserInDB

from . import schemas, services
from .models import RequestCreate


router = APIRouter(prefix="/api/recommender", tags=["recommender"])


@router.post('/', response_model=schemas.ResultResponse)
async def get_result(
        request: RequestCreate,
        current_user: UserInDB = Depends(get_current_user)
):
    request_in_db = await services.get_request(request, current_user)
    return await services.get_recomendations(request_in_db)


@router.get('/history', response_model=List[schemas.HistoryResponse])
async def get_history(current_user: UserInDB = Depends(get_current_user)):
    return await services.get_requests_history(current_user)


@router.delete('/{request_id}')
async def delete_request(
    request_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    if not await services.delete_request(current_user, request_id):
        raise HTTPException(
            status_code=400,
            detail='You can only delete your requests'
        )
    return {'message': 'Request deleted successfully'}
