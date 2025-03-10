from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from .admin import get_admin
from .service import (
    get_all_records, get_record, create_record, update_record, delete_record,
    get_all_users, get_user, create_user, update_user, delete_user
)
from fastapi import Request
from .admin import templates

admin = get_admin()
router = admin.router

@router.get("/")
async def admin_page(request: Request):
    """Главная страница админки"""
    return templates.TemplateResponse("index.html", {"request": request})

# 📌 CRUD для всех таблиц
@router.get("/{table_name}/")
async def get_all(table_name: str, db: AsyncSession = Depends(admin.get_db)):
    """Получить все записи из таблицы"""
    try:
        return await get_all_records(table_name, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{table_name}/{record_id}")
async def get_one(table_name: str, record_id: int, db: AsyncSession = Depends(admin.get_db)):
    """Получить конкретную запись по ID"""
    try:
        return await get_record(table_name, record_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{table_name}/")
async def create(table_name: str, data: Dict[str, Any], db: AsyncSession = Depends(admin.get_db)):
    """Создать новую запись"""
    try:
        return await create_record(table_name, data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{table_name}/{record_id}")
async def update(table_name: str, record_id: int, data: Dict[str, Any], db: AsyncSession = Depends(admin.get_db)):
    """Обновить существующую запись"""
    try:
        return await update_record(table_name, record_id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{table_name}/{record_id}")
async def delete(table_name: str, record_id: int, db: AsyncSession = Depends(admin.get_db)):
    """Удалить запись"""
    try:
        return await delete_record(table_name, record_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 📌 CRUD для пользователей
@router.get("/users/")
async def get_all_users_route(db: AsyncSession = Depends(admin.get_db)):
    """Получить всех пользователей"""
    return await get_all_users(db)

@router.get("/users/{user_id}")
async def get_user_route(user_id: int, db: AsyncSession = Depends(admin.get_db)):
    """Получить пользователя по ID"""
    return await get_user(user_id, db)

@router.post("/users/")
async def create_user_route(data: Dict[str, Any], db: AsyncSession = Depends(admin.get_db)):
    """Создать пользователя"""
    return await create_user(data, db)

@router.put("/users/{user_id}")
async def update_user_route(user_id: int, data: Dict[str, Any], db: AsyncSession = Depends(admin.get_db)):
    """Обновить пользователя"""
    return await update_user(user_id, data, db)

@router.delete("/users/{user_id}")
async def delete_user_route(user_id: int, db: AsyncSession = Depends(admin.get_db)):
    """Удалить пользователя"""
    return await delete_user(user_id, db)
