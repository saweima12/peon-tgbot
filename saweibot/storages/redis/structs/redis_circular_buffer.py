from redis.asyncio import Redis
from typing import List, Any

from .base import RedisObjectBase

class RedisCircularBuffer(RedisObjectBase):

    def __init__(self, namespace:str, size: int, redis: Redis):
        self.size = size
        super().__init__(namespace, redis)

    async def append(self, item):
        await self.redis.lpush(self.namespace, item)
        await self.redis.ltrim(self.namespace, 0, self.size - 1)

    @property
    async def length(self) -> int:
        return await self.redis.llen(self.namespace)

    @property
    async def list(self) -> List[Any]:
        return await self.redis.lrange(self.namespace, 0, self.size)