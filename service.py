from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import Dict, Any, Type
from .admin import get_admin
from .auth import hash_password

admin = get_admin()
UserModel: Type = admin.user_model

async def get_all_records(table_name: str, db: AsyncSession):
    """Получить все записи из таблицы"""
    if table_name not in admin.models:
        raise ValueError(f"Модель '{table_name}' не найдена")

    model = admin.models[table_name]
    result = await db.execute(select(model))
    return result.scalars().all()

async def get_record(table_name: str, record_id: int, db: AsyncSession):
    """Получить конкретную запись по ID"""
    if table_name not in admin.models:
        raise ValueError(f"Модель '{table_name}' не найдена")

    model = admin.models[table_name]
    record = await db.get(model, record_id)
    if not record:
        raise ValueError(f"Запись {record_id} не найдена в таблице '{table_name}'")
    return record

async def create_record(table_name: str, data: Dict[str, Any], db: AsyncSession):
    """Создать новую запись"""
    if table_name not in admin.models:
        raise ValueError(f"Модель '{table_name}' не найдена")

    model = admin.models[table_name]
    instance = model(**data)
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance

async def update_record(table_name: str, record_id: int, data: Dict[str, Any], db: AsyncSession):
    """Обновить существующую запись"""
    record = await get_record(table_name, record_id, db)

    for key, value in data.items():
        setattr(record, key, value)

    await db.commit()
    await db.refresh(record)
    return record

async def delete_record(table_name: str, record_id: int, db: AsyncSession):
    """Удалить запись"""
    record = await get_record(table_name, record_id, db)
    await db.delete(record)
    await db.commit()
    return {"message": f"Запись {record_id} удалена из '{table_name}'"}

# 📌 CRUD для пользователей
async def get_all_users(db: AsyncSession):
    """Получить всех пользователей"""
    result = await db.execute(select(UserModel))
    return result.scalars().all()

async def get_user(user_id: int, db: AsyncSession):
    """Получить пользователя по ID"""
    user = await db.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

async def create_user(data: Dict[str, Any], db: AsyncSession):
    """Создать пользователя"""
    if "password" in data:
        data["hashed_password"] = hash_password(data.pop("password"))
    user = UserModel(**data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(user_id: int, data: Dict[str, Any], db: AsyncSession):
    """Обновить пользователя"""
    user = await get_user(user_id, db)

    for key, value in data.items():
        if key == "password":
            value = hash_password(value)
            key = "hashed_password"
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(user_id: int, db: AsyncSession):
    """Удалить пользователя"""
    user = await get_user(user_id, db)
    await db.delete(user)
    await db.commit()
    return {"message": f"Пользователь {user_id} удалён"}
    