from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LLM_PROVIDER_URL: str
    LLM_API_KEY: str
    LLM_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
