from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.database import connect_to_mongo, close_mongo_connection

from apps.users.routers import router as auth_router
from apps.databases.routers import router as db_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="SmartReqs Service",
    description="Сервис автоматического определения стека технологий по описанию проекта",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(db_router)


@app.get("/")
async def root():
    return {"message": "Service is running"}
