from aiogram.types import Message, ChatType

from saweibot.peon_bot.data.wrappers.chat_config import ChatConfigWrapper

from .data.base import Status
from .data.wrappers.user_whitelist import ChatWhitelistWrapper

class MessageHelepr():
    
    def __init__(self, bot_id: str, message: Message):
        self.bot_id = bot_id
        self.msg = message
        self.chat = message.chat
        self.user = message.from_user

    @property
    def chat_id(self):
        return str(self.chat.id)
    
    @property
    def user_id(self):
        return str(self.user.id)

    @property
    def is_chat_group(self) -> bool:
        return self.msg.chat.type == ChatType.GROUP or \
            self.msg.chat.type == ChatType.SUPERGROUP

    async def is_whitelist_user(self) -> bool:
        wrapper = ChatWhitelistWrapper(self.bot_id)
        _model = await wrapper.get_model()
        return _model.whitelist_map.get(self.user_id) == Status.OK

    async def is_chat_registed(self):
        wrapper = ChatConfigWrapper(self.bot_id, self.chat_id)
        return await wrapper.proxy.exists()