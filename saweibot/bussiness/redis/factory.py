from redis.asyncio import Redis

from saweibot.db import redis

from .types.redis_circular_buffer import RedisCircularBuffer

class ContextFactory:

    def __init__(self, conn: Redis=None):
        # get default redis connection.
        self.conn = conn if conn else redis.get_db()

    def get_chatgroup_msgbuf(self, chat_id: str, size: int):
        _namespace= f"{chat_id}:msgbuf"
        return RedisCircularBuffer(_namespace, size, self.conn)

    def get_chatgroup_config(self, chat_id:str):
        _namespace = f"{chat_id}:config"
    
    def get_chatgroup_permission(self, chat_id:str):
        _nammespace = f"{chat_id}:per"
