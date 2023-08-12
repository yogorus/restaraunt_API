"""Menu Service layer"""
import json

from fastapi import BackgroundTasks, Depends

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

    async def add_count_children(self, data: dict) -> dict:
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
        cached_data = await self.redis.get_menu_by_id_from_cache(menu_id=kwargs['id'])

        if cached_data:
            return json.loads(cached_data)

        menu = await super().get_one(**kwargs)

        if count_children:
            menu = await self.add_count_children(menu)

        await self.redis.set_menu_to_cache(menu, menu_id=kwargs['id'])

        return menu

    async def create_menu(
        self,
        menu_data: menu_schemas.MenuBase,
        background_tasks: BackgroundTasks,
        count_children: bool = False,
        **kwargs
    ) -> dict:
        """Create menu and return dict"""

        menu = await super().create_obj(menu_data)

        if count_children:
            menu = await self.add_count_children(menu)

        background_tasks.add_task(self.redis.invalidate_menu_list)
        # await self.redis.invalidate_menu_list()

        return menu

    async def update_menu(
        self,
        menu_data: menu_schemas.MenuBase,
        background_task: BackgroundTasks,
        count_children: bool = False,
        **kwargs
    ) -> dict:
        """Update menu and return dict"""
        menu = await super().update_obj(menu_data, **kwargs)

        if count_children:
            menu = await self.add_count_children(menu)

        # Update cached menu by id and invalidate menu list
        # await self.redis.delete_menu_from_cache(menu_id=menu["id"])
        background_task.add_task(self.redis.delete_menu_from_cache, menu_id=menu['id'])

        return menu

    async def delete_menu(self, background_tasks: BackgroundTasks, **kwargs) -> dict:
        """Delete menu"""
        # await self.redis.delete_menu_from_cache(menu_id=kwargs["id"])
        background_tasks.add_task(
            self.redis.delete_menu_from_cache, menu_id=kwargs['id']
        )
        return await super().delete_obj(**kwargs)
