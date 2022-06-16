from saweibot.common.wrapper import StorageJsonModelWrapper

from ..entities import UserWhitelist
from ..models import StatusMapModel

class UserWhitelistWrapper(StorageJsonModelWrapper[StatusMapModel]):

    __model__ = StatusMapModel

    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        super().__init__()

    def _proxy(self):
        return self.factory(prefix=self.bot_id).get_json_obj("__user_whitelist")

    async def _from_proxy(self):
        result = await self.proxy.get()
        if result:
            return StatusMapModel(**result)
        return None

    async def _from_db(self):
        result = await UserWhitelist.filter(status="True")
        if result:
            whitelist_map = { item.chat_id: item.status for item in result}
            return StatusMapModel(_map=whitelist_map)
        return None

    async def _save_proxy(self, data: StatusMapModel=None, **kwargs):
        await self.proxy.set(data.dict())

    async def _save_db(self, data: StatusMapModel=None, **kwargs):
        for user_id, status in data.whitelist_map.items():
            await UserWhitelist.update_or_create({
                "status": status
            }, user_id=user_id)