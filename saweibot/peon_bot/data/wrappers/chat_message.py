from saweibot.core.wrapper import BaseModelWrapper
from saweibot.storages.redis import RedisCircularBuffer

from ..models import ChatMessageModel

class ChatMessageWrapper(BaseModelWrapper[ChatMessageModel, RedisCircularBuffer]):

    __model__ = ChatMessageModel

    def __init__(self, bot_id: str, chat_id: str, size: int):
        self.bot_id = bot_id
        self.chat_id = chat_id
        self.size = size
        super().__init__()

    def _proxy(self):
        return self.factory(self.bot_id).get_circular_buffer(self.size)

    async def _from_proxy(self):
        _data = await self.proxy.list()

    async def _save_proxy(self, data, **kwargs):
        return await super()._save_proxy(data, **kwargs)