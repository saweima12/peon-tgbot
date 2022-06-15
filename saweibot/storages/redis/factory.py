from webbrowser import get
from redis.asyncio import Redis

from saweibot.storages.redis.structs.redis_hash import RedisHashMap
from .structs.redis_json import RedisJsonObject
from .structs.redis_circular_buffer import RedisCircularBuffer

from .db import get_db

class RedisObjFactory:

    def __init__(self, conn: Redis=None, prefix: str=None):
        # get default redis connection.
        self.conn = conn if conn else get_db()
        self.prefix = prefix

    def get_json_obj(self, *args) -> RedisJsonObject:
        _namespace = self._get_namespace(*args)
        return RedisJsonObject(_namespace, self.conn)

    def get_circular_buffer(self, size: int, *args) -> RedisCircularBuffer:
        _namespace = self._get_namespace(*args)
        return RedisCircularBuffer(_namespace, size, self.conn)

    def get_hash_map(self, *args) -> RedisHashMap:
        _namespace = self._get_namespace(*args)
        return RedisHashMap(_namespace, self.conn)

    def _get_namespace(self, *args):
        str_args = ":".join([str(x) for x in args])
        return f"{self.prefix}:{str_args}"