from redis.asyncio import Redis

from saweibot.db import redis

from .types.circular_buffer import RedisCircularBuffer

class RedisContextFactory:

    def __init__(self, conn: Redis):
        self.conn = conn

    @classmethod
    async def create(cls, conn: Redis=None):
        """
        Create RedisContextFactory by asynchronous
        """
        # get default redis connection.
        if not conn:
            _redis = await redis.get_db()
            return RedisContextFactory(_redis)

        return RedisContextFactory(conn)

    async def get_chatmsg_buffer(self, chat_id: str, size: int):
        _namespace= f"{chat_id}:msg"
        return RedisCircularBuffer(_namespace, size, self.conn)

    async def get_chatgroup_config(self, chat_id:str):
        _namespace = f"{chat_id}:config"
    
    async def get_chatgroup_permission(self, chat_id:str):
        _nammespace = f"{chat_id}:per"
    