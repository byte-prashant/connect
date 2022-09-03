from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    TOKEN_URL: str = "/api/v1/profile/login"
    AWS_ACCESS_KEY: str
    AWS_SECRET: str
    AWS_BUCKET: str
    AWS_REGION: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_SID: str
    BASE_URL: AnyHttpUrl = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()