"""CRUD operations for Menu"""
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import Row, delete, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Dish, Menu, Submenu
from src.services.base.base_crud_repository import BaseCRUDRepository


class MenuCRUDRepository(BaseCRUDRepository):
    """CRUD layer for menu"""

    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
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

    async def delete_unspecified(self, id_list: list[UUID]) -> None:
        """Delete unspecified menus"""
        if not id_list:
            raise HTTPException(422, detail='ID list is empty!')

        stmt = delete(Menu).where(~Menu.id.in_(id_list))
        await self.session.execute(stmt)
        await self.session.commit()
