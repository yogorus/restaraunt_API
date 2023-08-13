"""CRUD to get everything from the database"""
from collections.abc import Sequence

from fastapi import Depends
from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.models import Menu, Submenu
from src.services.base.base_crud_repository import BaseCRUDRepository


class GeneralCRUDRepository(BaseCRUDRepository):
    """CRUD layer for getting everything"""

    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        super().__init__(session)
        self.model = Menu

    async def get_everything(self) -> Sequence[Row[tuple[Menu]]]:
        """Get every menu with all children"""
        query = await self.session.execute(
            select(Menu).options(joinedload(Menu.submenus).joinedload(Submenu.dishes))
        )
        result = query.unique().fetchall()
        return result
