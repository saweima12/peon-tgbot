from sanic import Sanic
from tortoise.contrib.pydantic import pydantic_model_creator

from saweibot.core.entities import BotConfig

from . import bot, meta, view
from .data.models import PeonBotConfig

def register_bot(app: Sanic, orm_modules: dict):

    @app.after_server_start
    async def setup(app, loop):
        # setup bot
        await bot.setup(app)

        # if it doesn't register, register it by default config.
        if not await BotConfig.exists(bot_id=meta.SERVICE_CODE):
            await BotConfig.create(
                bot_id=meta.SERVICE_CODE, 
                conf_json=PeonBotConfig().dict(),
                attach_json={}
            )
       
    @app.before_server_stop
    async def dispose(app, loop):
        await bot.dispose(app)

    # register extra entities.
    orm_modules["peon_entitles"] = ["saweibot.peon_bot.data.entities"]

    # register route
    app.blueprint(view.bp)
