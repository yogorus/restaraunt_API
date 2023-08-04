"""Menu Service layer"""
from fastapi import Depends

from src.schemas import menu_schemas
from src.services.menu.menu_repository import MenuCRUDRepository


class MenuService:
    """Service designed to return dicts and then pass them to pydantic"""

    def __init__(self, database_repository: MenuCRUDRepository = Depends()) -> None:
        self.database_repository = database_repository

    async def add_count_children(self, **data) -> dict:
        """func to count children"""

        count = await self.database_repository.count_children(menu_id=data['id'])
        data_count = count._asdict()

        data.update(data_count)

        return data

    async def get_list(self, count_children: bool = False) -> list[dict]:
        """return list of menus"""

        menus = await self.database_repository.get_list()
        data_list = []
        for menu in menus:
            data = {**menu.__dict__}

            if count_children:
                data = await self.add_count_children(**data)

            data_list.append(data)

        return data_list

    async def get_menu(
        self,
        count_children: bool = False,
        **kwargs,
    ) -> dict:
        """Get single menu"""
        menu = await self.database_repository.get_menu(**kwargs)
        data = {**menu.__dict__}

        if count_children:
            data = await self.add_count_children(**data)

        return data

    async def create_menu(
        self,
        menu_data: menu_schemas.MenuBase,
        count_children: bool = False,
    ) -> dict:
        """Create menu"""
        menu = await self.database_repository.create_menu(menu_data)
        data = {**menu.__dict__}

        if count_children:
            data = await self.add_count_children(**data)

        return data

    async def patch_menu(
        self, menu_data: menu_schemas.MenuBase, count_children: bool = False, **kwargs
    ) -> dict:
        """Update menu by passed data"""
        menu = await self.database_repository.patch_menu(menu_data, **kwargs)

        data = {**menu.__dict__}

        if count_children:
            data = await self.add_count_children(**data)

        return data

    async def delete_menu(self, **kwargs) -> dict:
        """Delete menu and return message"""
        await self.database_repository.delete_menu(**kwargs)
        return {'status': True, 'message': 'The menu has been deleted'}
