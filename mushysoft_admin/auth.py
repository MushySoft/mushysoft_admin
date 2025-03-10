from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from .admin import get_admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def hash_password(password: str) -> str:
    """Возвращает хешированный пароль"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля и его хеша"""
    return pwd_context.verify(plain_password, hashed_password)

def create_token(user_id: int, is_superuser: bool) -> str:
    """Генерирует JWT-токен"""
    admin = get_admin()
    expiration = datetime.now() + timedelta(minutes=admin.token_expiration_minutes)
    payload = {"sub": user_id, "exp": expiration, "superuser": is_superuser}
    return jwt.encode(payload, admin.secret_key, algorithm="HS256")

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    """Проверяет JWT-токен и возвращает текущего суперюзера"""
    admin = get_admin()
    try:
        payload = jwt.decode(token, admin.secret_key, algorithms=["HS256"])
        if not payload.get("superuser"):
            raise HTTPException(status_code=403, detail="Требуется суперюзер")
        return {"admin_id": payload["sub"], "superuser": True}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Недействительный токен")
