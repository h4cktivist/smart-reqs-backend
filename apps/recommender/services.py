from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import HTTPException, status

from apps.users.models import UserInDB
from core.database import get_requests_collection, get_results_collection
from .models import RequestInDB, RequestCreate
from .schemas import ResultResponse, HistoryResponse
from .utils import get_project_info_from_llm, get_recommended_techs, filter_recommended_techs_with_llm


async def get_request(request: RequestCreate, current_user: UserInDB) -> RequestInDB:
    collection = get_requests_collection()
    req_dict = request.dict()

    if any([v is None for v in req_dict.values()]):
        llm_res_dict = await get_project_info_from_llm(req_dict['idea_description'], req_dict['functional_reqs'])
        if not llm_res_dict['status']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request does not match the IT projects topic"
            )

        req_dict.update((k, v) for k, v in llm_res_dict.items() if k in req_dict and req_dict[k] is None)
    req_dict['user_id'] = current_user.id
    req_dict['datetime'] = datetime.now()

    result = await collection.insert_one(req_dict)
    inserted_req = await collection.find_one({"_id": result.inserted_id})
    return RequestInDB(**inserted_req)


async def get_recomendations(request: RequestInDB) -> ResultResponse:
    collection = get_results_collection()
    recomendation_result = await get_recommended_techs(request.dict())
    filtered_recomendation_result = await filter_recommended_techs_with_llm(request.dict(), recomendation_result)
    filtered_recomendation_result['request_id'] = request.id

    result = await collection.insert_one(filtered_recomendation_result)
    inserted_result = await collection.find_one({"_id": result.inserted_id})
    return ResultResponse(**inserted_result)


async def get_requests_history(current_user: UserInDB) -> List[HistoryResponse]:
    requests_collection = get_requests_collection()
    results_collection = get_results_collection()

    current_user_requests = await requests_collection.find({'user_id': current_user.id}).sort('datetime', -1).to_list()
    history_list = []
    for req in current_user_requests:
        result_for_req = await results_collection.find_one({'request_id': str(req['_id'])})
        history = {
            'user_id': current_user.id,
            'request': RequestInDB(**req),
            'result': ResultResponse(**result_for_req) if result_for_req else None
        }
        history_list.append(history)
    return [HistoryResponse(**h) for h in history_list]


async def delete_request(current_user: UserInDB, request_id: str) -> bool:
    collection = get_requests_collection()
    result = await collection.delete_one({'_id': ObjectId(request_id), 'user_id': current_user.id})
    return result.deleted_count == 1
