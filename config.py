from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str
    TOKEN_EXPIRATION_MINUTES: int = 60
    DATABASE_URL: str

    class Config:
        env_file = os.path.join(os.getcwd(), ".env")

settings = Settings()


if not settings.SECRET_KEY:
    raise ValueError("SECRET_KEY не найден! Добавьте его в .env")
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL не найден! Добавьте его в .env")
