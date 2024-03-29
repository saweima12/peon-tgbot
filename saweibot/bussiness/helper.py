from re import L
from typing import List
from aiogram.types import Message, MessageEntity, ChatType

from saweibot.data.wrappers.behavior_record import BehaviorRecordWrapper
from saweibot.data.wrappers.url_blacklist import ChatUrlBlackListWrapper
from saweibot.data.wrappers.watch_user import ChatWatcherUserWrapper

from saweibot.data.base import Status
from saweibot.data.models import ChatMessageModel
from saweibot.data.wrappers.chat_config import ChatConfigWrapper
from saweibot.data.wrappers.chat_message import ChatMessageWrapper
from saweibot.data.wrappers.user_whitelist import UserWhitelistWrapper
from saweibot.data.wrappers.deleted_message import DeletedMessageWrapper

from saweibot.utils import has_url

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

    def is_bot(self) -> bool:
        return self.user.is_bot

    def is_super_group(self) -> bool:
        return self.chat.type == ChatType.SUPERGROUP

    def is_private_chat(self) -> bool:
        return self.chat.type == ChatType.PRIVATE
    
    def is_text(self) -> bool:
        return self.content_type == "text"

    def is_forward(self) -> bool:
        return self.msg.is_forward()

    def has_url(self) -> bool:
        if self.msg.entities:
            url_entites = [entity for entity in self.msg.entities if entity.type == "url"]
            if len(url_entites) > 0:
                return True

        if self.is_text():
            return has_url(self.msg.text)
        return False
    
    def get_mentions(self) -> List[MessageEntity]:
        if self.msg.entities:
            mention_entities = [entity for entity in self.msg.entities if entity.type == "mention"]
            if len(mention_entities) > 0:
                return mention_entities
        return None
    
    def get_custom_emoji(self) -> List[MessageEntity]:
        if self.msg.entities:
            emoji_entities = [entity for entity in self.msg.entities if entity.type == "custom_emoji"]
            if len(emoji_entities) > 0:
                return emoji_entities
        return None
        
    async def is_group_admin(self) -> bool:
        wrapper = self.chat_config_wrapper()
        config = await wrapper.get_model()
        return self.user_id in config.adminstrators

    async def is_whitelist_user(self) -> bool:
        wrapper = UserWhitelistWrapper(self.bot_id)
        _model = await wrapper.get_model()
        return _model.status_map.get(self.user_id) == Status.OK

    async def is_group_registered(self):
        wrapper = self.chat_config_wrapper()
        if await wrapper.proxy.exists():
            return await wrapper.proxy.get(".status") == Status.OK
        return False

    async def is_senior_member(self):
        behavior_wrapper = self.behavior_wrapper()
        chat_wrapper = self.chat_config_wrapper()
        record = await behavior_wrapper.get(self.user_id)
        chat_config = await chat_wrapper.get_model()
        # return behavior_count > chat_config.senior_count
        if record.msg_count >= chat_config.senior_count:
            return True
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

    def behavior_wrapper(self):
        return BehaviorRecordWrapper(self.bot_id, self.chat_id)

    def watcher_wrapper(self):
        return ChatWatcherUserWrapper(self.bot_id, self.chat_id)

    def url_blacklist_wrapper(self):
        return ChatUrlBlackListWrapper(self.bot_id, self.chat_id)

    async def chat_message_wrapper(self):
        config = await self.chat_config_wrapper().get_model()
        return ChatMessageWrapper(self.bot_id, config.buffer_size, self.chat_id)

    