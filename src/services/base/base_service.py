"""module with base dict service"""
from pydantic import BaseModel

from src.services.base.base_crud_repository import BaseCRUDRepository


class BaseService:
    """Service designed to return dicts and then pass them to pydantic"""

    def __init__(self, database_repository: BaseCRUDRepository) -> None:
        self.database_repository = database_repository

    async def get_list(self, **kwargs) -> list[dict]:
        """Return list of menu dicts"""

        obj_list = await self.database_repository.get_list(**kwargs)
        data_list = []

        for obj in obj_list:
            data = {**obj.__dict__}

            data_list.append(data)

        return data_list

    async def get_one(self, **kwargs) -> dict:
        """Get dict of one model"""
        obj = await self.database_repository.get_one(**kwargs)
        data = {**obj.__dict__}
        return data

    async def create_obj(self, input_data: BaseModel, **kwargs) -> dict:
        """Create object and return dict"""
        obj = await self.database_repository.create_object(input_data, **kwargs)
        output_data = {**obj.__dict__}
        return output_data

    async def update_obj(self, input_data: BaseModel, **kwargs) -> dict:
        """Update object and return dict"""
        obj = await self.database_repository.update_object(input_data, **kwargs)
        output_data = {**obj.__dict__}
        return output_data

    async def delete_obj(self, **kwargs) -> dict:
        """Delete object and return message"""
        obj = await self.database_repository.delete_object(**kwargs)
        return {'status': True, 'message': f'the {obj} has been deleted'}
