"""Redis base cache module"""
import json
import types

import aioredis

from src.config import REDIS_CACHE_TIME, REDIS_HOST, REDIS_PORT

if REDIS_CACHE_TIME:
    expire = int(REDIS_CACHE_TIME)


class CacheEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles circular references"""

    def default(self, o):
        """Without this thing encoding gets stuck in the recursive loop"""
        if isinstance(o, types.GeneratorType):
            return list(o)
        try:
            json.dumps(o)
            return o
        except TypeError:
            return str(o)


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
        data = json.dumps(value, cls=CacheEncoder)
        await self.redis.set(key, data)
        await self.redis.expire(key, self.expire)

    async def delete_from_cache(self, *keys) -> None:
        """delete from cache"""
        await self.redis.delete(*keys)

    async def get_matched_keys(self, pattern: str) -> set:
        """Fetch keys that match the pattern"""
        keys = set()
        async for key in self.redis.scan_iter(match=pattern):
            keys.add(key)
        return keys
