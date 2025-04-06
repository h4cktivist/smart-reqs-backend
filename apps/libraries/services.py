from typing import List, Optional
from bson import ObjectId

from core.database import get_library_collection
from .models import LibraryInDB, LibraryCreate, LibraryUpdate


async def create_library(library: LibraryCreate) -> LibraryInDB:
    collection = get_library_collection()
    lib_dict = library.dict()
    result = await collection.insert_one(lib_dict)
    new_lib = await collection.find_one({"_id": result.inserted_id})
    return LibraryInDB(**new_lib)


async def get_library(library_id: str) -> Optional[LibraryInDB]:
    collection = get_library_collection()
    lib = await collection.find_one({"_id": ObjectId(library_id)})
    return LibraryInDB(**lib) if lib else None


async def get_all_libraries() -> List[LibraryInDB]:
    collection = get_library_collection()
    return [LibraryInDB(**lib) async for lib in collection.find()]


async def update_library(library_id: str, library: LibraryUpdate) -> Optional[LibraryInDB]:
    collection = get_library_collection()
    update_data = {k: v for k, v in library.dict().items() if v is not None}

    if len(update_data) == 0:
        return None

    result = await collection.update_one(
        {"_id": ObjectId(library_id)},
        {"$set": update_data}
    )
    if result.modified_count == 1:
        return await get_library(library_id)
    return None


async def delete_library(library_id: str) -> bool:
    collection = get_library_collection()
    result = await collection.delete_one({"_id": ObjectId(library_id)})
    return result.deleted_count == 1
