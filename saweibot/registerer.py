import asyncio
from sanic import Sanic, response
from sanic.exceptions import BadURL
from saweibot import views
from saweibot.data.entities import PeonChatConfig
from saweibot.data.wrappers.chat_config import ChatConfigWrapper
from saweibot.services import redis, scheduler, bot, opencc
from saweibot.bussiness.task import check_watchlist, proxy_to_db, cache_group_admin, load_config

from .meta import SERVICE_CODE


def setup(app: Sanic, orm_modules: dict):
    # register service.
    redis.register(app)
    opencc.register(app)
    
    _scheduler = scheduler.register(app)
    _bot = bot.register(app)
    
    # register extra entities.
    orm_modules["peon_entitles"] = ["saweibot.data.entities"]

    # register view route
    views.register_route(app)

    # register once task
    load_config.register_task(_scheduler)

    # register scheudle task.
    check_watchlist.register_task(_scheduler)
    proxy_to_db.register_task(_scheduler)
    cache_group_admin.register_task(_scheduler)

    @app.main_process_start
    async def setup(app, loop):
        # register webhook.
        await bot.set_webhook(app, _bot)
       
    @app.before_server_stop
    async def dispose(app, loop):
        await bot.dispose(app)


    # handle exception.
    @app.exception([BadURL, Exception])
    async def handle_badurl(request, exception):
        return response.empty(status=500)
