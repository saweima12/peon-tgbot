from saweibot.common.redis.structs.redis_hash import RedisHashMap
from saweibot.common.wrapper import BaseModelWrapper
from saweibot.data.models import ChatBehaviorRecordModel
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
            _data = ChatBehaviorRecordModel.parse_raw(result)
            return _data

        result = await ChatBehaviorRecord.get_or_none(chat_id=self.chat_id, user_id=user_id)
        if result:
            return ChatBehaviorRecordModel(full_name=result.full_name, msg_count=result.msg_count)

        return ChatBehaviorRecordModel()


    async def set(self, user_id: str, data: ChatBehaviorRecordModel):
        await self.proxy.set_key(user_id, data.json())


    async def save_db(self, user_id: str, data: ChatBehaviorRecordModel, **kwargs):
        await ChatBehaviorRecord.update_or_create({
            'full_name': data.full_name,
            "msg_count": data.msg_count
        }, chat_id=self.chat_id, user_id=user_id)

    async def save_all_db(self):
        result = await self.proxy.getall()
        for uid, item in result.items():
            _uid = uid.decode()
            obj = ChatBehaviorRecordModel.parse_raw(item)

            await ChatBehaviorRecord.update_or_create({
                'full_name': obj.full_name,
                'msg_count': obj.msg_count
            }, chat_id=self.chat_id, user_id=_uid)
    
    async def delete_proxy(self):
        await self.proxy.delete()