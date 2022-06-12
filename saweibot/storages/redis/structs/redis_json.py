import orjson as json
from redis.asyncio import Redis

class RedisJsonObject(object):
    
    def __init__(self, namespace:str, redis: Redis):
        self.namespace = namespace
        self.redis = redis

    async def set(self, obj: dict, path="."):
        await self.redis.json().set(self.namespace, path, obj)

    async def get(self, path="."):
        return await self.redis.json().get(self.namespace, path)

    async def arrindex(self, value, path=".", **kwargs):
        return await self.redis.json().arrindex(self.namespace, path, value, **kwargs)