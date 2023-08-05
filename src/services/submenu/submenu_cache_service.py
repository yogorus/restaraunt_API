"""Module that provides all of the caching operation for Submenu Service"""
# from uuid import UUID

from fastapi import Depends

from src.services.base.base_cache_service import BaseCacheService
from src.services.menu.menu_cache_service import MenuCacheService


class SubmenuCacheService(BaseCacheService):
    """Menu caching methods"""

    def __init__(self, menu_cache_service: MenuCacheService = Depends()):
        super().__init__()
        self.parent_cache_service = menu_cache_service

    async def invalidate_submenu_list(self, data: dict) -> None:
        """Delete menu list from cache"""
        await self.delete_from_cache('submenu_list')

        # Invalidate parent
        await self.parent_cache_service.get_menu_list_from_cache()
        await self.parent_cache_service.delete_menu_from_cache(data['menu_id'])
