from typing import List, Optional
from bson import ObjectId

from core.database import get_database_collection
from .models import DatabaseInDB, DatabaseCreate, DatabaseUpdate


async def create_database(database: DatabaseCreate) -> DatabaseInDB:
    collection = get_database_collection()
    db_dict = database.dict()
    result = await collection.insert_one(db_dict)
    new_db = await collection.find_one({"_id": result.inserted_id})
    return DatabaseInDB(**new_db)


async def get_database(database_id: str) -> Optional[DatabaseInDB]:
    collection = get_database_collection()
    db = await collection.find_one({"_id": ObjectId(database_id)})
    return DatabaseInDB(**db) if db else None


async def get_all_databases() -> List[DatabaseInDB]:
    collection = get_database_collection()
    return [DatabaseInDB(**db) async for db in collection.find()]


async def update_database(database_id: str, database: DatabaseUpdate) -> Optional[DatabaseInDB]:
    collection = get_database_collection()
    update_data = {k: v for k, v in database.dict().items() if v is not None}

    if len(update_data) == 0:
        return None

    result = await collection.update_one(
        {"_id": ObjectId(database_id)},
        {"$set": update_data}
    )
    if result.modified_count == 1:
        return await get_database(database_id)
    return None


async def delete_database(database_id: str) -> bool:
    collection = get_database_collection()
    result = await collection.delete_one({"_id": ObjectId(database_id)})
    return result.deleted_count == 1
