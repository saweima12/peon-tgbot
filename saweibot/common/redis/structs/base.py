from abc import ABCMeta
from redis.asyncio import Redis

class RedisObjectBase(metaclass=ABCMeta):

    def __init__(self, namespace: str, redis: Redis):
        self.__namespace = namespace
        self.__redis = redis

    @property
    def redis(self):
        return self.__redis

    @property
    def namespace(self):
        return self.__namespace

    async def exists(self):
        # return False
        return (await self.__redis.exists(self.__namespace)) > 0
    
    async def delete(self):
        return await self.__redis.delete(self.__namespace)