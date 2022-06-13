import orjson as json
from redis.asyncio import Redis
from .base import RedisObjectBase

class RedisJsonObject(RedisObjectBase):
    
    async def set(self, obj: dict, path="."):
        await self.redis.json().set(self.namespace, path, obj)

    async def get(self, path="."):
        return await self.redis.json().get(self.namespace, path)

    async def arrindex(self, value, path=".", **kwargs):
        return await self.redis.json().arrindex(self.namespace, path, value, **kwargs)