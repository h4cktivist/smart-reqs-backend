from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import connect_to_mongo, close_mongo_connection

from apps.users.routers import router as auth_router
from apps.databases.routers import router as db_router
from apps.frameworks.routers import router as fr_router
from apps.libraries.routers import router as lib_router
from apps.recommender.routers import router as rec_router
from apps.expert.routers import router as exp_router


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(db_router)
app.include_router(fr_router)
app.include_router(lib_router)
app.include_router(rec_router)
app.include_router(exp_router)


@app.get("/")
async def root():
    return {"message": "Service is running"}
