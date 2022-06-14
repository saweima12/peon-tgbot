from saweibot.core.wrapper import BaseModelWrapper
from saweibot.storages.redis import RedisCircularBuffer

from ..models import ChatMessageModel

class ChatMessageWrapper(BaseModelWrapper[RedisCircularBuffer]):

    def __init__(self, bot_id: str, size: int, chat_id: str):
        self.bot_id = bot_id
        self.size = size
        self.chat_id = chat_id
        self._buffer = None
        super().__init__()

    def _proxy(self):
        return self.factory(self.bot_id).get_circular_buffer(self.size, self.chat_id)

    async def list(self):
        if not self._buffer:
            self._buffer = await self.proxy.list()
        return self._buffer

    async def append(self, data: ChatMessageModel):
        await self.proxy.append(data.dict())