"""Module that provides all of the caching operation for Menu Service"""
from src.services.base.base_cache_service import BaseCacheService


class MenuCacheService(BaseCacheService):
    """Menu caching methods"""

    async def invalidate_menu_list(self) -> None:
        """Delete menu list from cache"""
        await self.delete_from_cache('menu_list')
        await self.delete_from_cache('get_all')

    async def get_menu_list_from_cache(self) -> str:
        """Get menu list from cache"""
        menu_key = 'menu_list'
        return await self.get_from_cache(menu_key)

    async def get_menu_by_id_from_cache(self, **kwargs) -> str:
        """Get single menu from cache"""
        menu_key = f'menu_{kwargs["menu_id"]}'
        return await self.get_from_cache(menu_key)

    async def set_menu_list_to_cache(self, data: list[dict]) -> None:
        """Sets all menus to cache"""
        menu_key = 'menu_list'
        return await self.set_to_cache(menu_key, data)

    async def set_menu_to_cache(self, data: dict, **kwargs) -> None:
        """Sets menu to cache and invalidates list cache"""
        menu_key = f"menu_{kwargs['menu_id']}"
        await self.invalidate_menu_list()
        await self.set_to_cache(menu_key, data)

    async def delete_menu_from_cache(self, **kwargs) -> None:
        """Deletes menu from cache and invalidates list cache and child cache"""
        menu_key = f"menu_{kwargs['menu_id']}"
        await self.invalidate_menu_list()
        await self.delete_from_cache(menu_key)

        # Delete all children from cache, like cascade in sql
        child_keys = await self.get_matched_keys(f"{kwargs['menu_id']}_*")
        if child_keys:
            await self.delete_from_cache(*child_keys)
