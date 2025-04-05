from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings


class Database:
    client: AsyncIOMotorClient = None


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: str = None) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId: {value}")
        return ObjectId(value)


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
