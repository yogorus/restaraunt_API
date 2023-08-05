"""CRUD operations for Menu"""
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Row, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Dish, Menu, Submenu
from src.services.base.base_crud_repository import BaseCRUDRepository


class MenuCRUDRepository(BaseCRUDRepository):
    """CRUD layer for menu"""

    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        # self.session: AsyncSession = session
        super().__init__(session)
        self.model = Menu

    async def count_children(self, menu_id: UUID) -> Row[tuple[int, int]]:
        """Count children of Menu object by id"""
        # pylint: disable=E1102

        query = await self.session.execute(
            select(
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .select_from(Menu)
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .filter(Menu.id == menu_id)
        )

        result = query.one()
        return result
