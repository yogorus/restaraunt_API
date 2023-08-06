"""CRUD operations for Submenu"""
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import Row, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Dish, Submenu
from src.schemas.submenu_schemas import SubmenuBase
from src.services.base.base_crud_repository import BaseCRUDRepository
from src.services.menu.menu_repository import MenuCRUDRepository


class SubmenuCRUDRepository(BaseCRUDRepository):
    """CRUD layer for submenu"""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db),
        menu_repository: MenuCRUDRepository = Depends(),
    ) -> None:
        super().__init__(session)
        self.model = Submenu
        self.parent_repository = menu_repository

    async def count_same_titles(self, title: str) -> int:
        """Count submenus that have the same title"""
        # pylint: disable=E1102

        query = await self.session.execute(
            select(func.count(distinct(Submenu.title)).label('title_count')).filter(
                Submenu.title == title
            )
        )
        result = query.scalar_one()
        return result

    async def count_children(self, submenu_id: UUID) -> Row[tuple[int]]:
        """Count dishes of submenu"""
        # pylint: disable=E1102

        query = await self.session.execute(
            select(func.count(distinct(Dish.id)).label('dishes_count'))
            .select_from(Submenu)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .filter(Submenu.id == submenu_id)
        )

        result = query.one()

        return result

    async def create_object(self, data: SubmenuBase, **kwargs) -> Submenu:
        """Validate for titles before creation"""
        if await self.count_same_titles(data.title) >= 1:
            raise HTTPException(409, detail='submenu with that title already exists')

        return await super().create_object(data, **kwargs)

    async def update_object(self, data: SubmenuBase, **kwargs) -> Submenu:
        """Validate titles before updating submenu"""
        if await self.count_same_titles(data.title) > 1:
            raise HTTPException(409, detail='submenu with that title already exists')

        return await super().update_object(data, **kwargs)
