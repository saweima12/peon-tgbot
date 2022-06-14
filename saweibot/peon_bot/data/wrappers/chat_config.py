from saweibot.core.wrapper import JsonModelWrapper

from ..entities import PeonChatConfig
from ..models import ChatConfigModel

class ChatConfigWrapper(JsonModelWrapper[ChatConfigModel]):

    __model__ = ChatConfigModel

    def __init__(self, bot_id: str, chat_id: str):
        self.bot_id = bot_id
        self.chat_id = str(chat_id)
        super().__init__()

    def _proxy(self):
        return self.factory(self.bot_id).get_json_obj(f"{self.chat_id}:config")

    async def _from_proxy(self):
        result = await self.proxy.get()
        if result:
            return ChatConfigModel(**result)
        return None

    async def _from_db(self):
        result = await PeonChatConfig.get_or_none(chat_id=self.chat_id)
        if result:
            data = ChatConfigModel(**result.config_json)
            return data
        return None

    async def _save_proxy(self, data: ChatConfigModel, **kwargs):
        await self.proxy.set(data.dict())

    async def _save_db(self, data: ChatConfigModel, **kwargs):
        await PeonChatConfig.update_or_create({
            'config_json': data.dict()
        }, chat_id=self.chat_id)