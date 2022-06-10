import asyncio
from redis.asyncio import Redis

class RedisCircularBuffer(object):

    def __init__(self, namespace:str, size: int, redis: Redis):
        self.namespace = namespace
        self.size = size
        self.redis = redis

    async def append(self, item):
        await self.redis.lpush(self.namespace, item)
        await self.redis.ltrim(self.namespace, 0, self.size - 1)

    @property
    async def length(self):
        return await self.redis.llen(self.namespace)

    @property
    async def list(self):
        return await self.redis.lrange(self.namespace, 0, self.size)