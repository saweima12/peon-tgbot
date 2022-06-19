from .base import RedisObjectBase

from typing import Any, Mapping

class RedisHashMap(RedisObjectBase):

    async def get(self, key: str):
        return await self.redis.hget(self.namespace, key)

    async def getall(self):
        return await self.redis.hgetall(self.namespace)

    async def set_key(self, key: str, value: Any, mapping: Mapping=None):
        return await self.redis.hset(self.namespace, key, value)

    async def exists_key(self, key: str):
        return await self.redis.hexists(self.namespace, key)

    async def delete_key(self, key: str):
        return await self.redis.hdel(self.namespace, key)

    async def keys(self):
        return await self.redis.hkeys(self.namespace)