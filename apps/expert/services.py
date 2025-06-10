from typing import List

from bson import ObjectId

from apps.expert.schemas import ExpertResponse
from apps.recommender.models import RequestInDB
from core.database import get_requests_collection, get_results_collection


async def get_unanswered_requests() -> List[RequestInDB]:
    requests_collection = get_requests_collection()
    results_collection = get_results_collection()

    empty_results = await results_collection.find({
        'frameworks': [],
        'libraries': [],
        'databases': []
    }).to_list()
    request_list = []
    for er in empty_results:
        req_for_res = await requests_collection.find_one({'_id': ObjectId(er['request_id'])})
        if req_for_res:
            request_list.append(RequestInDB(**req_for_res))
    return request_list


async def answer_request(request_id: str, expert_response: ExpertResponse):
    results_collection = get_results_collection()

    empty_result = await results_collection.find_one({'request_id': request_id})
    if empty_result:
        empty_result['frameworks'] = expert_response.frameworks if expert_response.frameworks is not None else empty_result['frameworks']
        empty_result['libraries'] = expert_response.libraries if expert_response.libraries is not None else empty_result['libraries']
        empty_result['databases'] = expert_response.databases if expert_response.databases is not None else empty_result['databases']
        empty_result['min_devs'] = expert_response.min_devs if expert_response.min_devs is not None else empty_result['min_devs']
        empty_result['max_devs'] = expert_response.max_devs if expert_response.max_devs is not None else empty_result['max_devs']
        await results_collection.update_one({'request_id': request_id}, {'$set': empty_result})
    else:
        result = expert_response.dict()
        result['request_id'] = request_id
        await results_collection.insert_one(result)
    return {'detail': 'Success'}

