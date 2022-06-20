from sanic import Sanic

from saweibot.common.entities import BotConfig
from saweibot.services import redis, scheduler

from saweibot.data.models import BotConfigModel
from saweibot.data.wrappers import BotConfigWrapper
from saweibot.views import bot as bot_view

from .meta import SERVICE_CODE
from . import bot

def setup(app: Sanic, orm_modules: dict):
    # register redis
    redis.register(app)
    scheduler.register(app)

    # setup bot
    instance = bot.setup(app)
    
    @app.after_server_start
    async def setup(app, loop):
        # register webhook.
        await bot.set_webhook(app, instance)
        # add to redis
        await BotConfigWrapper(SERVICE_CODE).load()

        # if it doesn't register to db, register it by default config.
        if not await BotConfig.exists(bot_id=SERVICE_CODE):
            await BotConfig.create(
                bot_id=SERVICE_CODE, 
                conf_json=BotConfigModel().dict(),
                attach_json={}
            )

       
    @app.before_server_stop
    async def dispose(app, loop):
        await bot.dispose(app)

    # register extra entities.
    orm_modules["peon_entitles"] = ["saweibot.data.entities"]

    # register view route
    app.blueprint(bot_view.bp)
