from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue

from .config import settings


class Database:
    client: AsyncIOMotorClient = None


class PyObjectId(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {"type": "string", "format": "objectid"}

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        import pydantic_core.core_schema as core_schema

        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: Any) -> str:
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return str(v)


db = Database()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URI)


async def close_mongo_connection():
    db.client.close()


def get_database():
    return db.client[settings.MONGO_DB]


def get_user_collection():
    return get_database()["users"]


def get_database_collection():
    return get_database()["databases"]


def get_framework_collection():
    return get_database()["frameworks"]


def get_library_collection():
    return get_database()["libraries"]


def get_requests_collection():
    return get_database()["requests"]
