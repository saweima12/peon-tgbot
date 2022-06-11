from webbrowser import get
from redis.asyncio import Redis
from .structs.redis_json import RedisJsonObject
from .structs.redis_circular_buffer import RedisCircularBuffer

from .db import get_db

class RedisObjFactory:

    def __init__(self, conn: Redis=None, prefix: str=None):
        # get default redis connection.
        self.conn = conn if conn else get_db()
        self.prefix = prefix

    def get_json_obj(self, *args):
        _namespace = self._get_namespace(*args)
        return RedisJsonObject(_namespace, self.conn)

    def get_circular_buffer(self, size: int, *args):
        _namespace = self._get_namespace(*args, "msgbuf")
        return RedisCircularBuffer(_namespace, size, self.conn)

    def _get_namespace(self, *args):
        str_args = ":".join([str(x) for x in args])
        return f"{self.prefix}:{str_args}"