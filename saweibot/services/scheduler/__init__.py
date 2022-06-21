from sanic import Sanic
from . import scheduler

from .struct import AppScheduler
from .scheduler import get

def register(app: Sanic) -> AppScheduler:

    _scheduler = scheduler.setup(app)

    @app.after_server_start
    async def startup(app: Sanic, _):
        await _scheduler.run_scheduler(app)


    @app.before_server_stop
    async def dispose(app: Sanic, _):
        await _scheduler.stop_scheduler()

    return _scheduler