from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from .admin import init_admin, get_admin

class CRUDHandler:
    def __init__(self):
        self.admin = get_admin()

    async def create_record(self, table: str, data: Dict[str, Any]):
        model = self.admin.models.get(table)
        if not model:
            raise ValueError(f"Модель '{table}' не найдена")

        instance = model(**data)
        async with self.admin.get_db() as db:
            db.add(instance)
            await db.commit()
            await db.refresh(instance)
        return instance

    async def get_all_records(self, table: str):
        model = self.admin.models.get(table)
        if not model:
            raise ValueError(f"Модель '{table}' не найдена")

        async with self.admin.get_db() as db:
            result = await db.execute(model.__table__.select())
            return result.scalars().all()

    async def get_record(self, table: str, record_id: int):
        model = self.admin.models.get(table)
        if not model:
            raise ValueError(f"Модель '{table}' не найдена")

        async with self.admin.get_db() as db:
            result = await db.get(model, record_id)
            if not result:
                raise ValueError(f"Запись {record_id} не найдена в таблице '{table}'")
            return result

    async def update_record(self, table: str, record_id: int, data: Dict[str, Any]):
        model = self.admin.models.get(table)
        if not model:
            raise ValueError(f"Модель '{table}' не найдена")

        async with self.admin.get_db() as db:
            record = await db.get(model, record_id)
            if not record:
                raise ValueError(f"Запись {record_id} не найдена в таблице '{table}'")

            for key, value in data.items():
                setattr(record, key, value)

            await db.commit()
            await db.refresh(record)
        return record

    async def delete_record(self, table: str, record_id: int):
        model = self.admin.models.get(table)
        if not model:
            raise ValueError(f"Модель '{table}' не найдена")

        async with self.admin.get_db() as db:
            record = await db.get(model, record_id)
            if not record:
                raise ValueError(f"Запись {record_id} не найдена в таблице '{table}'")

            await db.delete(record)
            await db.commit()
        return {"message": f"Запись {record_id} удалена из '{table}'"}
