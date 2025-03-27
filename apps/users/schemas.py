from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserResponse(BaseModel):
    username: str
    email: str
    is_expert: bool


class UserLoginRequest(BaseModel):
    email: str
    password: str
