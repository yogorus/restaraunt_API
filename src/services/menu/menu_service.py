"""Menu Service layer"""
import json

from fastapi import Depends

from src.schemas import menu_schemas
from src.services.base.base_service import BaseService
from src.services.menu.menu_cache_service import MenuCacheService
from src.services.menu.menu_repository import MenuCRUDRepository


class MenuService(BaseService):
    """Menu service converting db to dict"""

    def __init__(
        self,
        database_repository: MenuCRUDRepository = Depends(),
        redis: MenuCacheService = Depends(),
    ) -> None:
        super().__init__(database_repository)
        self.database_repository: MenuCRUDRepository = database_repository
        self.redis = redis

    async def add_count_children(self, data: dict) -> dict[str, int]:
        """func to count children"""

        count = await self.database_repository.count_children(menu_id=data['id'])
        data_count = count._asdict()

        data.update(data_count)

        return data

    async def get_menus(self, count_children: bool = False) -> list[dict]:
        """Get list of menus"""
        cached_data = await self.redis.get_menu_list_from_cache()

        if cached_data:
            return json.loads(cached_data)

        menus = await super().get_list()

        if count_children:
            for i, menu in enumerate(menus):
                menus[i] = await self.add_count_children(menu)

        await self.redis.set_menu_list_to_cache(menus)

        return menus

    async def get_menu(self, count_children: bool = False, **kwargs) -> dict:
        """Get single menu"""
        cached_data = await self.redis.get_menu_by_id_from_cache(kwargs['id'])

        if cached_data:
            return json.loads(cached_data)

        menu = await super().get_one(**kwargs)

        if count_children:
            menu = await self.add_count_children(menu)

        await self.redis.set_menu_to_cache(menu)

        return menu

    async def create_menu(
        self, menu_data: menu_schemas.MenuBase, count_children: bool = False
    ) -> dict:
        """Create menu and return dict"""
        menu = await super().create_obj(menu_data)

        if count_children:
            menu = await self.add_count_children(menu)

        await self.redis.set_menu_to_cache(menu)

        return menu

    async def update_menu(
        self, menu_data: menu_schemas.MenuBase, count_children: bool = False, **kwargs
    ) -> dict:
        """Update menu and return dict"""
        menu = await super().update_obj(menu_data, **kwargs)

        if count_children:
            menu = await self.add_count_children(menu)

        # Update cached menu by id and invalidate menu list
        await self.redis.set_menu_to_cache(menu)

        return menu

    async def delete_obj(self, **kwargs) -> dict:
        await self.redis.delete_from_cache(f"menu_{kwargs['id']}")
        await self.redis.delete_from_cache('menu_list')
        return await super().delete_obj(**kwargs)
