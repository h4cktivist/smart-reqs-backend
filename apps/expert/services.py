from typing import List

from bson import ObjectId

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

