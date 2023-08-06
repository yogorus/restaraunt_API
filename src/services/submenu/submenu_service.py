"""Submenu Service layer"""
import json

from fastapi import Depends

from src.schemas.submenu_schemas import SubmenuBase, SubmenuForeignKey
from src.services.base.base_service import BaseService
from src.services.submenu.submenu_cache_service import SubmenuCacheService
from src.services.submenu.submenu_repository import SubmenuCRUDRepository


class SubmenuService(BaseService):
    """Submenu service converting db to dict"""

    def __init__(
        self,
        database_repository: SubmenuCRUDRepository = Depends(),
        redis: SubmenuCacheService = Depends(),
    ) -> None:
        super().__init__(database_repository)
        self.database_repository: SubmenuCRUDRepository = database_repository
        self.redis = redis

    async def add_count_children(self, data: dict) -> dict:
        """Function to count dishes"""

        count = await self.database_repository.count_children(submenu_id=data['id'])
        data_count = count._asdict()

        data.update(data_count)

        return data

    async def get_submenus(self, count_children: bool = False, **kwargs) -> list[dict]:
        """Get list of submenu dicts"""
        cached_data = await self.redis.get_submenu_list_from_cache(
            menu_id=kwargs['menu_id']
        )
        if cached_data:
            return json.loads(cached_data)

        submenus = await super().get_list(**kwargs)

        if count_children:
            for i, menu in enumerate(submenus):
                submenus[i] = await self.add_count_children(menu)

        await self.redis.set_submenu_list_to_cache(submenus, **kwargs)

        return submenus

    async def get_submenu(self, count_children: bool = False, **kwargs) -> dict:
        """Get submenu dict"""
        cached_data = await self.redis.get_submenu_from_cache(
            submenu_id=kwargs['id'], menu_id=kwargs['menu_id']
        )

        if cached_data:
            return json.loads(cached_data)

        submenu = await super().get_one(**kwargs)

        if count_children:
            submenu = await self.add_count_children(submenu)

        await self.redis.set_submenu_to_cache(
            submenu, menu_id=submenu['menu_id'], submenu_id=['id']
        )

        return submenu

    async def create_submenu(
        self, submenu_data: SubmenuBase, count_children: bool = False, **kwargs
    ) -> dict:
        """Create Submenu and return dict"""
        submenu_data = SubmenuForeignKey(
            **submenu_data.model_dump(), menu_id=kwargs['menu_id']
        )
        submenu = await super().create_obj(submenu_data, **kwargs)

        if count_children:
            submenu = await self.add_count_children(submenu)

        await self.redis.invalidate_submenu_list(
            menu_id=kwargs['menu_id'], submenu_id=submenu['id']
        )

        return submenu

    async def update_submenu(
        self, submenu_data: SubmenuBase, count_children: bool = False, **kwargs
    ) -> dict:
        """Update Submenu and return dict"""
        submenu = await super().update_obj(submenu_data, **kwargs)

        if count_children:
            submenu = await self.add_count_children(submenu)

        await self.redis.delete_submenu_from_cache(
            menu_id=kwargs['menu_id'], submenu_id=submenu['id']
        )

        return submenu

    async def delete_obj(self, **kwargs) -> dict:
        await self.redis.delete_submenu_from_cache(
            submenu_id=kwargs['id'], menu_id=kwargs['menu_id']
        )
        return await super().delete_obj(**kwargs)
