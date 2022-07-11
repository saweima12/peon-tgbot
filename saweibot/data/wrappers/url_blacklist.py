from saweibot.common.wrapper import StorageJsonModelWrapper
from ..entities import ChatUrlBlackList
from ..models import ChatUrlBlackListModel

class UrlBlackListWrapper(StorageJsonModelWrapper[ChatUrlBlackListModel]):
    
    def __init__(self, bot_id: str, chat_id: str):
        self.bot_id = bot_id
        self.chat_id = chat_id
        super().__init__()

    def _proxy(self):
        return self.factory(prefix=self.bot_id).get_json_obj(self.chat_id, "url_black_list")

    async def _from_proxy(self):
        result = await self.proxy.get()
        if result:
            return ChatUrlBlackListModel(**result)
        return None

    async def _from_db(self):
        result = await ChatUrlBlackList.get_or_none(chat_id=self.chat_id)
        if result:
            return ChatUrlBlackListModel(pattern_list=result.pattern_list)
        return None

    async def _save_proxy(self, data: ChatUrlBlackListModel, **kwargs):
        await self.proxy.set(data.dict())


    async def _save_db(self, data: ChatUrlBlackListModel, **kwargs):
        await ChatUrlBlackList.update_or_create(defaults={"pattern_list": data.pattern_list}, chat_id=self.chat_id)