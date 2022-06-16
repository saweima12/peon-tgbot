import orjson
from redis.asyncio import Redis
from typing import List, Any, Dict

from .base import RedisObjectBase

class RedisCircularBuffer(RedisObjectBase):

    def __init__(self, namespace:str, size: int, redis: Redis):
        self.size = size
        super().__init__(namespace, redis)

    async def append(self, item: Dict[str, Any]):
        item = orjson.dumps(item)
        await self.redis.lpush(self.namespace, item)
        await self.redis.ltrim(self.namespace, 0, self.size - 1)

    async def length(self) -> int:
        return await self.redis.llen(self.namespace)

    async def list(self) -> List[Any]:
        return await self.redis.lrange(self.namespace, 0, self.size - 1)

    async def last(self) -> Any:
        return await self.redis.lindex(self.namespace, self.size - 1)

    async def first(self) -> Any:
        return await self.redis.lindex(self.namespace, 0)
