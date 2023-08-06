"""Dish cache module"""
from fastapi import Depends

from src.services.base.base_cache_service import BaseCacheService
from src.services.submenu.submenu_cache_service import SubmenuCacheService


class DishCacheService(BaseCacheService):
    """Dish caching methods"""

    def __init__(self, submenu_cache_service: SubmenuCacheService = Depends()):
        super().__init__()
        self.parent_cache_service = submenu_cache_service
