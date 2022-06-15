from re import L
from aiogram.types import Message, ChatType, ContentTypes


from .data.base import Status
from .data.models import ChatMessageModel
from .data.wrappers.chat_config import ChatConfigWrapper
from .data.wrappers.chat_message import ChatMessageWrapper
from .data.wrappers.user_whitelist import UserWhitelistWrapper
from .data.wrappers.deleted_message import DeletedMessageWrapper

class MessageHelepr():
    
    def __init__(self, bot_id: str, message: Message):
        self.bot_id = bot_id
        self.msg = message
        self.chat = message.chat
        self.user = message.from_user


    """
    Properties
    """
    @property
    def message_id(self):
        return str(self.msg.message_id)

    @property
    def chat_id(self):
        return str(self.chat.id)
    
    @property
    def user_id(self):
        return str(self.user.id)

    @property
    def content_type(self):
        return str(self.msg.content_type)

    @property
    def content(self) -> dict:
        return self.msg.to_python().get(self.content_type)

    @property
    def reply_msg(self):
        return self.msg.reply_to_message

    @property
    def bot(self):
        return self.msg.bot

    @property
    def message_model(self):
        return ChatMessageModel(message_id=self.message_id, 
                                content_type=self.content_type,
                                user_id=self.user_id, 
                                is_bot=self.is_bot(),
                                chat_id=self.chat_id, 
                                content=self.content)

    """
    Match
    """

    def is_bot(self):
        return self.user.is_bot

    def is_group(self) -> bool:
        return self.chat.type == ChatType.GROUP or \
            self.chat.type == ChatType.SUPERGROUP

    def is_private_chat(self):
        return self.chat.type == ChatType.PRIVATE
    
    def is_text(self):
        return self.content_type == "text"

    async def is_group_admin(self) -> bool:
        bot = self.msg.bot
        admin_list = await bot.get_chat_administrators(self.chat_id)
        admin_id_set = set([str(item.user.id) for item in admin_list])
        return self.user_id in admin_id_set

    async def is_whitelist_user(self) -> bool:
        wrapper = UserWhitelistWrapper(self.bot_id)
        _model = await wrapper.get_model()
        return _model.whitelist_map.get(self.user_id) == Status.OK

    async def is_group_registered(self):
        wrapper = self.chat_config_wrapper()
        if await wrapper.proxy.exists():
            return await wrapper.proxy.get(".status") == Status.OK
        return False

    """
    Get Wrapper
    """

    def chat_config_wrapper(self):
        return ChatConfigWrapper(self.bot_id, self.chat_id)

    def user_list_wrapper(self):
        return UserWhitelistWrapper(self.bot_id)

    def deleted_message_wrapper(self):
        return DeletedMessageWrapper(self.bot_id, self.chat_id)

    async def chat_message_wrapper(self):
        config = await self.chat_config_wrapper().get_model()
        return ChatMessageWrapper(self.bot_id, config.buffer_size, self.chat_id)
