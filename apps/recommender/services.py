from datetime import datetime

from fastapi import HTTPException, status

from apps.users.models import UserInDB
from core.database import get_requests_collection
from .models import RequestInDB, RequestCreate
from .utils import get_project_info_from_llm


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
