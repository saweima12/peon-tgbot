from typing import List
from saweibot.common.wrapper import BaseModelWrapper
from saweibot.common.redis import RedisCircularBuffer

from ..models import ChatMessageModel

class ChatMessageWrapper(BaseModelWrapper[RedisCircularBuffer]):

    def __init__(self, bot_id: str, size: int, chat_id: str):
        self.bot_id = bot_id
        self.size = size
        self.chat_id = chat_id
        self._buffer = None
        super().__init__()

    def _proxy(self):
        return self.factory(self.bot_id).get_circular_buffer(self.size, self.chat_id, "msgbuf")

    async def list(self) -> List[ChatMessageModel]:
        if not self._buffer:
            _buffer = await self.proxy.list()
            self._buffer = [ ChatMessageModel.parse_raw(item) for item in _buffer]
        return self._buffer

    async def last(self):
        item = await self.proxy.last()
        return ChatMessageModel.parse_raw(item)

    async def append(self, data: ChatMessageModel):
        await self.proxy.append(data.dict())

    async def will_overflow(self):
        return (await self.proxy.length()) >= self.size