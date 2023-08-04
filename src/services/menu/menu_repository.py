"""CRUD operations for Menu"""
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import Row, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Dish, Menu, Submenu
from src.schemas import menu_schemas


class MenuCRUDRepository:
    """Menu CRUD opetaions"""

    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.session: AsyncSession = session
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

    async def get_list(self, **kwargs) -> list[Menu]:
        """Get list of Menus from database"""

        query = await self.session.execute(select(Menu).filter_by(**kwargs))
        result = list(query.scalars().all())
        return result

    async def get_menu(self, **kwargs) -> Menu:
        """Get single Menu from database"""

        query = await self.session.execute(select(Menu).filter_by(**kwargs))
        result: Menu | None = query.scalar()

        if not result:
            raise HTTPException(status_code=404, detail='menu not found')

        return result

    async def create_menu(self, menu_data: menu_schemas.MenuBase) -> Menu:
        """Create Menu in database"""
        menu = Menu(**menu_data.model_dump())
        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def patch_menu(self, menu_data: menu_schemas.MenuBase, **kwargs) -> Menu:
        """Update existing Menu in database"""

        menu = await self.get_menu(**kwargs)
        menu_data_dict = menu_data.model_dump(exclude_unset=True)
        for key, value in menu_data_dict.items():
            setattr(menu, key, value)

        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def delete_menu(self, **kwargs) -> None:
        """Delete Menu from database"""

        menu = await self.get_menu(**kwargs)
        await self.session.delete(menu)
        await self.session.commit()
