from typing import List
from saweibot.core.wrapper import BaseModelWrapper
from saweibot.storages.redis import RedisHashMap

from ..models import ChatMessageModel

class DeletedMessageWrapper(BaseModelWrapper[RedisHashMap]):
    
    def __init__(self, bot_id: str, chat_id: str):
        self.bot_id = bot_id
        self.chat_id = chat_id

    def _proxy(self):
        return self.factory(self.bot_id).get_hash_map(self.chat_id, "deleted_map")

    async def exists(self, msg_id: str):
        return await self.proxy.exists_key(msg_id)

    async def get(self, msg_id: str):
        return await self.proxy.get(msg_id)

    async def keys(self):
        # will return bstr, need to decode.
        return [item.decode() for item in await self.proxy.keys()]

    async def append(self, msg_id: str, data: ChatMessageModel):
        return await self.proxy.set_key(msg_id, data)

    async def delete(self, msg_id: str):
        return await self.proxy.delete_key(msg_id)
    