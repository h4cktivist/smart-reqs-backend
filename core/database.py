from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URI)


async def close_mongo_connection():
    db.client.close()


def get_database():
    return db.client[settings.MONGO_DB]


def get_user_collection():
    return get_database()["users"]
