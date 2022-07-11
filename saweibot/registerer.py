from sanic import Sanic, response
from sanic.exceptions import BadURL
from saweibot import views
from saweibot.services import redis, scheduler, bot
from saweibot.bussiness.task import check_watchlist, proxy_to_db, cache_group_admin

from .meta import SERVICE_CODE


def setup(app: Sanic, orm_modules: dict):
    # register service.
    _redis = redis.register(app)
    _scheduler = scheduler.register(app)
    _bot = bot.register(app)
    
    @app.main_process_start
    async def setup(app, loop):
        # register webhook.
        await bot.set_webhook(app, _bot)
       
    @app.before_server_stop
    async def dispose(app, loop):
        await bot.dispose(app)

    # register extra entities.
    orm_modules["peon_entitles"] = ["saweibot.data.entities"]

    # register view route
    views.register_route(app)

    # register scheudle task.
    check_watchlist.register_task(_scheduler)
    proxy_to_db.register_task(_scheduler)
    cache_group_admin.register_task(_scheduler)

    # handle exception.
    @app.exception([BadURL, Exception])
    async def handle_badurl(request, exception):
        return response.empty(status=500)
