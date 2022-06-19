from datetime import datetime, timedelta
from sanic import Sanic
from saweibot.common.entities import BotConfig
from saweibot.services import scheduler

from . import bot, view
from .data import meta
from .data.models import BotConfigModel
from .data.wrappers import BotConfigWrapper

def register_bot(app: Sanic, orm_modules: dict):

    # setup bot
    instance = bot.setup(app)
    
    @app.after_server_start
    async def setup(app, loop):
        # register webhook.
        await bot.set_webhook(app, instance)
        # add to redis
        await BotConfigWrapper(meta.SERVICE_CODE).load()

        # if it doesn't register to db, register it by default config.
        if not await BotConfig.exists(bot_id=meta.SERVICE_CODE):
            await BotConfig.create(
                bot_id=meta.SERVICE_CODE, 
                conf_json=BotConfigModel().dict(),
                attach_json={}
            )

       
    @app.before_server_stop
    async def dispose(app, loop):
        await bot.dispose(app)

    # register extra entities.
    orm_modules["peon_entitles"] = ["saweibot.peon_bot.data.entities"]

    # register task
    _scheduler = scheduler.get()

    # @_scheduler.register_task(name="test", period=timedelta(seconds=1))
    # def test_task():
    #     print("test23")

    # register route
    app.blueprint(view.bp)