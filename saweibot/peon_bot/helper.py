from aiogram.types import Message, ChatType, ContentTypes
from saweibot.peon_bot.data.entities import UserWhitelist

from saweibot.peon_bot.data.wrappers.chat_config import ChatConfigWrapper

from .data.base import Status
from .data.wrappers.user_whitelist import UserWhitelistWrapper

class MessageHelepr():
    
    def __init__(self, bot_id: str, message: Message):
        self.bot_id = bot_id
        self.msg = message
        self.chat = message.chat
        self.user = message.from_user

    @property
    def message_id(self):
        return str(self.message_id)

    @property
    def chat_id(self):
        return str(self.chat.id)
    
    @property
    def user_id(self):
        return str(self.user.id)

    @property
    def is_bot(self):
        return self.user.is_bot

    @property
    def content_type(self):
        return self.msg.content_type

    @property
    def content(self):
        return 
    
    @property
    def is_group(self) -> bool:
        return self.chat.type == ChatType.GROUP or \
            self.chat.type == ChatType.SUPERGROUP

    @property
    def is_private_chat(self):
        return self.chat.type == ChatType.PRIVATE

    async def is_whitelist_user(self) -> bool:
        wrapper = UserWhitelistWrapper(self.bot_id)
        _model = await wrapper.get_model()
        return _model.whitelist_map.get(self.user_id) == Status.OK

    async def is_group_registed(self):
        wrapper = ChatConfigWrapper(self.bot_id, self.chat_id)
        print(await wrapper.proxy.exists())
        return await wrapper.proxy.exists()