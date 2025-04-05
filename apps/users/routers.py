from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta

from core.security import create_access_token
from core.config import settings
from . import schemas, services, models
from .dependencies import get_current_user


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserResponse)
async def register(user: models.UserCreate):
    return await services.create_user(user)


@router.post("/login", response_model=schemas.Token)
async def login(credentials: schemas.UserLoginRequest):
    user = await services.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user['email']},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
async def read_user_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    return current_user
