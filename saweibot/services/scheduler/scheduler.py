from sanic import Sanic

from .struct import AppScheduler

SERVICE_CODE = "app_scheduler"


def get_scheduler() -> AppScheduler:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

def setup(app: Sanic) -> AppScheduler:
    app = Sanic.get_app()
    scheduler = AppScheduler(app)
    setattr(app.ctx, SERVICE_CODE, scheduler)
    return scheduler

async def dispose(app: Sanic):
    if hasattr(app.ctx, SERVICE_CODE):
        _scheduler: AppScheduler = getattr(app.ctx, SERVICE_CODE)
        await _scheduler.stop_scheduler()