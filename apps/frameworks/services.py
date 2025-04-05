from typing import List, Optional
from bson import ObjectId

from core.database import get_framework_collection
from .models import FrameworkInDB, FrameworkCreate, FrameworkUpdate


async def create_framework(framework: FrameworkCreate) -> FrameworkInDB:
    collection = get_framework_collection()
    framework_dict = framework.dict()
    result = await collection.insert_one(framework_dict)
    new_framework = await collection.find_one({"_id": result.inserted_id})
    return FrameworkInDB(**new_framework)


async def get_framework(framework_id: str) -> Optional[FrameworkInDB]:
    collection = get_framework_collection()
    framework = await collection.find_one({"_id": ObjectId(framework_id)})
    return FrameworkInDB(**framework) if framework else None


async def get_all_frameworks() -> List[FrameworkInDB]:
    collection = get_framework_collection()
    return [FrameworkInDB(**framework) async for framework in collection.find()]


async def update_framework(framework_id: str, framework: FrameworkUpdate) -> Optional[FrameworkInDB]:
    collection = get_framework_collection()
    update_data = {k: v for k, v in framework.dict().items() if v is not None}

    if len(update_data) == 0:
        return None

    result = await collection.update_one(
        {"_id": ObjectId(framework_id)},
        {"$set": update_data}
    )
    if result.modified_count == 1:
        return await get_framework(framework_id)
    return None


async def delete_framework(framework_id: str) -> bool:
    collection = get_framework_collection()
    result = await collection.delete_one({"_id": ObjectId(framework_id)})
    return result.deleted_count == 1
