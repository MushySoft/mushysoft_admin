from fastapi import FastAPI, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import Dict, Type, Optional
from .config import settings
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

class CustomAdmin:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Создаёт синглтон: если уже есть экземпляр, возвращает его"""
        if cls._instance is None:
            cls._instance = super(CustomAdmin, cls).__new__(cls)
        return cls._instance

    def __init__(self, app: FastAPI, connection: AsyncSession, user_model: Type[DeclarativeBase]):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.__router = APIRouter()
        self.__models: Dict[str, Type[DeclarativeBase]] = {}
        self.__connection = connection
        self.__user_model = user_model
        self.__secret_key = settings.SECRET_KEY
        self.__token_expiration_minutes = settings.TOKEN_EXPIRATION_MINUTES
        self._initialized = True

        app.include_router(self.__router)

    def include_table(self, table: Type[DeclarativeBase]) -> None:
        """Добавляет таблицу в админку"""
        if not issubclass(table, DeclarativeBase):
            raise TypeError(f"Object {table} is not a SQLAlchemy model")

        if not hasattr(table, "__tablename__"):
            raise ValueError(f"Model {table} has no __tablename__ field")

        self.__models[table.__tablename__] = table

    @property
    def router(self) -> APIRouter:
        return self.__router

    @property
    def models(self) -> Dict[str, Type[DeclarativeBase]]:
        return self.__models

    @property
    def get_db(self):
        return self.__connection

    @property
    def user_model(self) -> Type[DeclarativeBase]:
        return self.__user_model

    @property
    def secret_key(self) -> str:
        return self.__secret_key

    @property
    def token_expiration_minutes(self) -> float:
        return self.__token_expiration_minutes


_admin_instance: Optional[CustomAdmin] = None

def init_admin(app: FastAPI, connection: AsyncSession, user_model: Type[DeclarativeBase]) -> CustomAdmin:
    """Функция для инициализации админки"""
    global _admin_instance
    if _admin_instance is None:
        _admin_instance = CustomAdmin(app, connection, user_model)
    return _admin_instance

def get_admin() -> CustomAdmin:
    """Функция для получения текущего экземпляра админки"""
    if _admin_instance is None:
        raise RuntimeError("Админка не была инициализирована. Вызовите init_admin() сначала.")
    return _admin_instance


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


def setup_static(app):
    app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")