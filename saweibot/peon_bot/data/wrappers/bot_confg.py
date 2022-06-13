from saweibot.core.entities import BotConfig
from saweibot.core.wrapper import BaseModelWrapper
from saweibot.storages.redis import RedisJsonObject

from ..models import BotConfigModel

class BotConfigWrapper(BaseModelWrapper[BotConfigModel, RedisJsonObject]):

    __model__ = BotConfigModel

    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        super().__init__()

    def _proxy(self) -> RedisJsonObject:
        return self.factory(self.bot_id).get_json_obj("config")

    async def _from_proxy(self):
        result = await self.proxy.get()
        if result:
            return BotConfigModel(**result)
        return None

    async def _from_db(self):
        result = await BotConfig.get_or_none(bot_id=self.bot_id)
        if result:
            return BotConfigModel(**result.conf_json)
        return None

    async def _save_proxy(self, data: BotConfigModel=None):
        await self.proxy.set(data.dict())
    
    async def _save_db(self, data: BotConfigModel=None):
        await BotConfig.update_or_create({
            'conf_json': data.dict()
        }, bot_id=self.bot_id)
