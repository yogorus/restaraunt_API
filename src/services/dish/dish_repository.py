"""CRUD operations for Dish"""
from fastapi import Depends, HTTPException
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Dish
from src.schemas.dish_schemas import DishBaseModel
from src.services.base.base_crud_repository import BaseCRUDRepository
from src.services.submenu.submenu_repository import SubmenuCRUDRepository


class DishCRUDRepository(BaseCRUDRepository):
    """CRUD layer for submenu"""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db),
        submenu_repository: SubmenuCRUDRepository = Depends(),
    ) -> None:
        super().__init__(session)
        self.model = Dish
        self.parent_repository = submenu_repository

    async def count_same_titles(self, title: str) -> int:
        """Count submenus that have the same title"""
        # pylint: disable=E1102

        query = await self.session.execute(
            select(func.count(distinct(Dish.title)).label('title_count')).filter(
                Dish.title == title
            )
        )
        result = query.scalar_one()
        return result

    async def create_object(self, data: DishBaseModel, **kwargs) -> Dish:
        """Validate for titles before creation"""
        if await self.count_same_titles(data.title) >= 1:
            raise HTTPException(409, detail='submenu with that title already exists')

        return await super().create_object(data, **kwargs)

    async def update_object(self, data: DishBaseModel, **kwargs) -> Dish:
        """Validate titles before updating submenu"""
        if await self.count_same_titles(data.title) > 1:
            raise HTTPException(409, detail='submenu with that title already exists')

        return await super().update_object(data, **kwargs)
