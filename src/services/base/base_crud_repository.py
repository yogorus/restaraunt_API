"""Base CRUD for inheritance"""
from typing import Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import Base

M = TypeVar(
    'M', bound=Base
)  # This type is all inheritants of SQLAlchemy Base, e.g Models
Schema = TypeVar('Schema', bound=BaseModel)  # Inheritants of Pydantic schemas


class BaseCRUDRepository(Generic[M, Schema]):
    """CRUD class with common methods to inherit from"""

    def __init__(self, session: AsyncSession):
        """init of the class"""
        self.session = session
        self.model: type[M]  # Define the model in the child class
        self.schema: type[Schema]
        self.parent_repository: BaseCRUDRepository[M, Schema] | None = None

    async def get_list(self, **kwargs) -> list[M]:
        """
        Get list of objects
        """
        query = await self.session.execute(select(self.model).filter_by(**kwargs))
        result = list(query.scalars().all())
        return result

    async def get_one(self, **kwargs) -> M:
        """
        Get one database instanse
        Raise exception of none
        """
        query = await self.session.execute(select(self.model).filter_by(**kwargs))
        result: M | None = query.scalar()

        if not result:
            raise HTTPException(
                status_code=404, detail=f'{self.model.__name__.lower()} not found'
            )

        return result

    async def create_object(self, data: Schema, **kwargs) -> M:
        """Create object from data dump"""
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update_object(self, data: Schema, **kwargs) -> M:
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
