from aiogram import Bot
from saweibot.storages.redis import RedisJsonObject

from saweibot.core.wrapper import BaseModelWrapper
from saweibot.core.entities import BotConfig

from ..models import BotConfigModel
from ..meta import SERVICE_CODE

class BotConfigWrapper(BaseModelWrapper):

    __model__ = BotConfigModel

    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        super().__init__()

    @property
    def proxy(self) -> RedisJsonObject:
        return self.factory(SERVICE_CODE).get_json_obj("config")

    async def from_proxy(self):
        result = await self.proxy.get()
        if result:
            return BotConfigModel(**result)
        return None

    async def from_db(self):
        result = await BotConfig.get_or_none(bot_id=self.bot_id)
        if result:
            return BotConfigModel(**result.conf_json)
        return None

    async def save(self, data: BotConfigModel=None):
        _data = data if data else (await self.get_model())
        await self.proxy.set(_data.json())
    
    async def save_db(self, data: BotConfigModel=None):
        _data = data if data else (await self.get_model())
        print(_data.dict(), self.bot_id)

        await BotConfig.update_or_create({
            'conf_json': _data.dict()
        }, bot_id=self.bot_id)