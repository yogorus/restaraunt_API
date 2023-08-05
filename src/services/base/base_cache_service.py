"""Redis base cache module"""
import json

import aioredis
from fastapi.encoders import jsonable_encoder

from src.config import REDIS_CACHE_TIME, REDIS_HOST, REDIS_PORT

if REDIS_CACHE_TIME:
    expire = int(REDIS_CACHE_TIME)


class BaseCacheService:
    """Base cache service to use in our services"""

    def __init__(self):
        self.redis = aioredis.from_url(f'{REDIS_HOST}://{REDIS_HOST}:{REDIS_PORT}')
        self.expire = expire

    async def get_from_cache(self, key: str) -> str:
        """set"""
        return await self.redis.get(key)

    async def set_to_cache(self, key: str, value: dict | list[dict]) -> None:
        """Set key-value to cache"""
        data = json.dumps(jsonable_encoder(value))
        await self.redis.set(key, data)
        await self.redis.expire(key, self.expire)

    async def delete_from_cache(self, key) -> None:
        """delete from cache"""
        await self.redis.delete(key)
