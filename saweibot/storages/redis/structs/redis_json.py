import orjson as json
from redis.asyncio import Redis
from redis.commands.json.path import Path


class RedisJsonObject(object):
    
    def __init__(self, namespace:str, redis: Redis):
        self.namespace = namespace
        self.redis = redis

    async def set(self, obj: dict):
        data = json.dumps(obj)
        self.redis.json().set(self.namespace, Path.root_path, data)

    async def get(self):
        return await self.redis.get(self.namespace)