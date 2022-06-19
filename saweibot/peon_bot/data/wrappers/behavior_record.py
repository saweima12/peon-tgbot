from saweibot.common.redis.structs.redis_hash import RedisHashMap
from saweibot.common.wrapper import BaseModelWrapper
from ..entities import ChatBehaviorRecord

class BehaviorRecordWrapper(BaseModelWrapper[RedisHashMap]):

    def __init__(self, bot_id: str, chat_id: str):
        self.bot_id = bot_id
        self.chat_id = chat_id

    def _proxy(self):
        return self.factory(self.bot_id).get_hash_map(self.chat_id, "behavior_record")

    async def exists(self, user_id: str):
        return self.proxy.exists_key(user_id)

    async def get(self, user_id: str):
        result = await self.proxy.get(user_id)
        if result:
            _data = int(result)
            return _data

        result = await ChatBehaviorRecord.get_or_none(chat_id=self.chat_id, user_id=user_id)
        if result:
            return int(result.msg_count)

        return 0


    async def set(self, user_id: str, count: int):
        await self.proxy.set_key(user_id, count)


    async def save_db(self, user_id: str, count: int, **kwargs):
        await ChatBehaviorRecord.update_or_create({
            "msg_count": count
        }, chat_id=self.chat_id, user_id=user_id)

    async def save_all_db(self):
        result = await self.proxy.getall()
        for uid, count in result.items():
            _uid = uid.decode()
            await ChatBehaviorRecord.update_or_create({
                'msg_count': count
            }, chat_id=self.chat_id, user_id=_uid)