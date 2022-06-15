from saweibot.core.wrapper import StorageJsonModelWrapper

from ..entities import UserWhitelist
from ..models import WhitelistModel

class UserWhitelistWrapper(StorageJsonModelWrapper[WhitelistModel]):

    __model__ = WhitelistModel

    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        super().__init__()

    def _proxy(self):
        return self.factory(prefix=self.bot_id).get_json_obj("__user_whitelist")

    async def _from_proxy(self):
        result = await self.proxy.get()
        if result:
            return WhitelistModel(**result)
        return None

    async def _from_db(self):
        result = await UserWhitelist.filter(status="True")
        if result:
            whitelist_map = { item.chat_id: item.status for item in result}
            return WhitelistModel(whitelist_map=whitelist_map)
        return None

    async def _save_proxy(self, data: WhitelistModel=None, **kwargs):
        await self.proxy.set(data.dict())

    async def _save_db(self, data: WhitelistModel=None, **kwargs):
        for user_id, status in data.whitelist_map.items():
            await UserWhitelist.update_or_create({
                "status": status
            }, user_id=user_id)