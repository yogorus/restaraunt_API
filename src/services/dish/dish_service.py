"""Dish service layers"""
import json

from fastapi import BackgroundTasks, Depends

from src.schemas.dish_schemas import DishBaseModel, DishForeignKey
from src.services.base.base_service import BaseService
from src.services.dish.dish_cache_service import DishCacheService
from src.services.dish.dish_repository import DishCRUDRepository


class DishService(BaseService):
    """Dish service converting db to dict, class specific methods need to pass parent id to check for their existence"""

    def __init__(
        self,
        database_repository: DishCRUDRepository = Depends(),
        redis: DishCacheService = Depends(),
    ) -> None:
        super().__init__(database_repository)
        self.database_repository: DishCRUDRepository = database_repository
        self.redis = redis

    async def get_dishes(self, filter_by_submenu: bool, **kwargs) -> list[dict]:
        """Get list of dish dicts of submenu parent"""
        cached_data = await self.redis.get_dish_list_from_cache(**kwargs)

        if cached_data:
            return json.loads(cached_data)

        if filter_by_submenu:
            dishes = await super().get_list(submenu_id=kwargs['submenu_id'])

        else:
            dishes = await super().get_list()

        await self.redis.set_dish_list_to_cache(dishes, **kwargs)

        return dishes

    async def get_dish(self, **kwargs) -> dict:
        """Get one dish dict"""

        cached_data = await self.redis.get_dish_from_cache(
            **kwargs, dish_id=kwargs['id']
        )

        if cached_data:
            return json.loads(cached_data)

        dish = await super().get_one(id=kwargs['id'])

        await self.redis.set_dish_to_cache(dish, dish_id=kwargs['id'], **kwargs)

        return dish

    async def create_dish(
        self, dish_data: DishBaseModel, background_tasks: BackgroundTasks, **kwargs
    ) -> dict:
        """Create dish and return dict"""
        background_tasks.add_task(self.redis.invalidate_dish_list, **kwargs)

        dish_data = DishForeignKey(
            **dish_data.model_dump(), submenu_id=kwargs['submenu_id']
        )

        dish = await super().create_obj(dish_data)

        return dish

    async def update_dish(
        self, dish_data: DishBaseModel, background_tasks: BackgroundTasks, **kwargs
    ) -> dict:
        """Update dish and return dict"""
        background_tasks.add_task(
            self.redis.delete_dish_from_cache, dish_id=kwargs['id'], **kwargs
        )
        dish_data.id = kwargs['id']
        dish_data = DishForeignKey(
            **dish_data.model_dump(), submenu_id=kwargs['submenu_id']
        )

        dish = await super().update_obj(dish_data, id=kwargs['id'])
        return dish

    async def delete_dish(self, background_tasks: BackgroundTasks, **kwargs) -> dict:
        """Delete dish"""
        background_tasks.add_task(
            self.redis.delete_dish_from_cache, dish_id=kwargs['id'], **kwargs
        )
        return await super().delete_obj(id=kwargs['id'])
