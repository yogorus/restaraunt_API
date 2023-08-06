"""Module that provides all of the caching operation for Submenu Service"""
from fastapi import Depends

from src.services.base.base_cache_service import BaseCacheService
from src.services.menu.menu_cache_service import MenuCacheService


class SubmenuCacheService(BaseCacheService):
    """Dish caching methods"""

    def __init__(self, menu_cache_service: MenuCacheService = Depends()):
        super().__init__()
        self.parent_cache_service = menu_cache_service

    async def invalidate_submenu_list(self, **kwargs) -> None:
        """Delete submenu list from cache and invalidate parent"""
        key = f"{kwargs['menu_id']}_submenu_list"
        await self.delete_from_cache(key)

        # Invalidate parent
        await self.parent_cache_service.delete_menu_from_cache(**kwargs)

    async def get_submenu_list_from_cache(self, **kwargs) -> str:
        """Get submenus of parent menu"""
        key = f"{kwargs['menu_id']}_submenu_list"
        return await self.get_from_cache(key)

    async def get_submenu_from_cache(self, **kwargs) -> str:
        """Get submenu from cache"""
        key = f"{kwargs['menu_id']}_submenu_{kwargs['submenu_id']}"
        return await self.get_from_cache(key)

    async def set_submenu_list_to_cache(self, data: list[dict], **kwargs) -> None:
        """Set submenu list and invalidate menu cache"""
        key = f"{kwargs['menu_id']}_submenu_list"
        await self.set_to_cache(key, data)
        await self.parent_cache_service.delete_menu_from_cache(**kwargs)

    async def set_submenu_to_cache(self, data: dict, **kwargs) -> None:
        """Set submenu to cache and invalidate parent submenu_list cache"""
        key = f"{kwargs['menu_id']}_submenu_{kwargs['submenu_id']}"
        await self.invalidate_submenu_list(menu_id=kwargs['menu_id'])
        await self.set_to_cache(key, data)

    async def delete_submenu_from_cache(self, **kwargs) -> None:
        """Deletes submenu from cache and invalidates parent menu cache and submenu_list"""
        key = f"{kwargs['menu_id']}_submenu_{kwargs['submenu_id']}"

        await self.invalidate_submenu_list(menu_id=kwargs['menu_id'])
        await self.delete_from_cache(key)
