import orjson
from saweibot.core.wrapper import BaseModelWrapper

from ..entities import ChatWhitelist
from ..models import ChatWhitelistModel

from ..meta import SERVICE_CODE

class ChatWhitelistWrapper(BaseModelWrapper):

    __model__ = ChatWhitelistModel

    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        super().__init__()

    @property
    def proxy(self):
        return self.factory(prefix=self.bot_id).get_json_obj("chat_whitelist")

    async def from_proxy(self):
        result = await self.proxy.get()
        if result:
            return ChatWhitelistModel(**result)
        return None

    async def from_db(self):
        result = await ChatWhitelist.filter(status="True")
        print(result)
        if result:
            whitelist_map = { item.chat_id: item.status for item in result}
            print(whitelist_map)
            return ChatWhitelistModel(whitelist_map=whitelist_map)
        return None

    async def save(self, data: ChatWhitelistModel=None, **kwargs):
        _data = data if data else (await self.load())
        await self.proxy.set(obj=_data.dict())

    async def save_db(self, data: ChatWhitelistModel=None, **kwargs):
        _data = data if data else (await self.load())
        for chat_id, status in _data.whitelist_map.items():
            data = {
                "status": status
            }
            print(data)
            await ChatWhitelist.update_or_create(data, chat_id=chat_id)