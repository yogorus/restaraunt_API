"""Dish service layers"""
from fastapi import Depends

from src.schemas.dish_schemas import DishBaseModel, DishForeignKey
from src.services.base.base_service import BaseService
from src.services.dish.dish_repository import DishCRUDRepository


class DishService(BaseService):
    """Dish service converting db to dict, class specific methods need to pass parent id to check for their existence"""

    def __init__(
        self,
        database_repository: DishCRUDRepository = Depends(),
        # redis: SubmenuCacheService = Depends(),
    ) -> None:
        super().__init__(database_repository)
        self.database_repository: DishCRUDRepository = database_repository
        # self.redis = redis

    async def get_dishes(self, **kwargs) -> list[dict]:
        """Get list of dish dicts of submenu parent"""

        return await super().get_list(**kwargs)

    async def get_dish(self, **kwargs) -> dict:
        """Get one dish dict"""

        return await super().get_one(**kwargs)

    async def create_dish(self, dish_data: DishBaseModel, **kwargs) -> dict:
        """Create dish and return dict"""

        dish_data = DishForeignKey(
            **dish_data.model_dump(), submenu_id=kwargs['submenu_id']
        )

        dish = await super().create_obj(dish_data, **kwargs)

        return dish

    async def update_dish(self, dish_data: DishBaseModel, **kwargs) -> dict:
        """Update dish and return dict"""

        dish_data = DishForeignKey(
            **dish_data.model_dump(), submenu_id=kwargs['submenu_id']
        )

        dish = await super().update_obj(dish_data)

        return dish

    async def delete_obj(self, **kwargs) -> dict:
        # await self.redis.delete_menu_from_cache(kwargs['id'])
        return await super().delete_obj(**kwargs)
