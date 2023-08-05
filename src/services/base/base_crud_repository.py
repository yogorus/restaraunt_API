"""Base CRUD for inheritance"""
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import Base


class BaseCRUDRepository:
    """CRUD class with common methods to inherit from"""

    def __init__(self, session: AsyncSession):
        """init of the class"""
        self.session = session
        self.model = Base  # Define the model in the child class

    async def get_list(self, **kwargs) -> list[Base]:
        """Get list of objects"""
        query = await self.session.execute(select(self.model).filter_by(**kwargs))
        result = list(query.scalars().all())
        return result

    async def get_one(self, **kwargs) -> Base:
        """Get one database instanse"""
        query = await self.session.execute(select(self.model).filter_by(**kwargs))
        result: Base | None = query.scalar()

        if not result:
            raise HTTPException(
                status_code=404, detail=f'{self.model.__name__.lower()} not found'
            )

        return result

    async def create_object(self, data: BaseModel) -> Base:
        """Create object from data dump"""
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update_object(self, data: BaseModel, **kwargs) -> Base:
        """Update object from data dump"""
        obj = await self.get_one(**kwargs)
        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete_object(self, **kwargs) -> str:
        """Delete single object from the database"""
        obj = await self.get_one(**kwargs)
        await self.session.delete(obj)
        await self.session.commit()
        return self.model.__name__.lower()
