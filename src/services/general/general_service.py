import json

from fastapi import Depends

from src.schemas.menu_schemas import MenuGeneral
from src.services.base.base_cache_service import BaseCacheService
from src.services.base.base_service import BaseService
from src.services.general.general_repository import GeneralCRUDRepository


class GeneralService(BaseService):
    """Menu service converting db to dict"""

    def __init__(
        self,
        database_repository: GeneralCRUDRepository = Depends(),
        redis: BaseCacheService = Depends(),
    ) -> None:
        super().__init__(database_repository)
        self.database_repository: GeneralCRUDRepository = database_repository
        self.redis = redis

    async def get_all(self) -> list[MenuGeneral]:
        """Get all menus with every child and convert those into pydantic model"""

        cached_data = await self.redis.get_from_cache('get_all')

        if cached_data:
            return json.loads(cached_data)

        data = await self.database_repository.get_everything()

        result = []

        for row in data:
            row_dict = row._asdict()
            menu_dict = row_dict['Menu']
            result.append(MenuGeneral.model_validate(menu_dict))

        await self.redis.set_to_cache('get_all', [item.__dict__ for item in result])
        return result
