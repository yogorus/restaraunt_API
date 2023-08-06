"""Dish cache module"""
from fastapi import Depends

from src.services.base.base_cache_service import BaseCacheService
from src.services.submenu.submenu_cache_service import SubmenuCacheService


class DishCacheService(BaseCacheService):
    """Dish caching methods"""

    def __init__(self, submenu_cache_service: SubmenuCacheService = Depends()):
        super().__init__()
        self.parent_cache_service = submenu_cache_service

    async def invalidate_dish_list(self, **kwargs) -> None:
        """Invalidate dish list and parents"""
        key = f"{kwargs['menu_id']}_{kwargs['submenu_id']}_dish_list"
        await self.delete_from_cache(key)
        await self.parent_cache_service.delete_submenu_from_cache(**kwargs)

    async def set_dish_list_to_cache(self, data: list[dict], **kwargs) -> None:
        """Invalidate parents and set dish list to cache"""
        key = f"{kwargs['menu_id']}_{kwargs['submenu_id']}_dish_list"
        await self.parent_cache_service.delete_submenu_from_cache(**kwargs)
        await self.set_to_cache(key, data)

    async def set_dish_to_cache(self, data: dict, **kwargs) -> None:
        """Invalidate parents and set dish to cache"""
        key = f"{kwargs['menu_id']}_{kwargs['submenu_id']}_{kwargs['dish_id']}"
        await self.set_to_cache(key, data)

    async def get_dish_from_cache(self, **kwargs) -> str:
        """Get dish from cache"""
        key = f"{kwargs['menu_id']}_{kwargs['submenu_id']}_{kwargs['dish_id']}"
        return await self.get_from_cache(key)

    async def get_dish_list_from_cache(self, **kwargs) -> str:
        """Get dish list from cache"""
        key = f"{kwargs['menu_id']}_{kwargs['submenu_id']}_dish_list"
        return await self.get_from_cache(key)

    async def delete_dish_from_cache(self, **kwargs) -> None:
        """Delete dish from cache and invalidate dish list and parents"""
        key = f"{kwargs['menu_id']}_{kwargs['submenu_id']}_{kwargs['dish_id']}"
        await self.delete_from_cache(key)
        await self.invalidate_dish_list(**kwargs)
