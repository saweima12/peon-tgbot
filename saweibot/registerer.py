from sanic import Sanic

from .services import redis, scheduler

from . import peon_bot

def setup(app: Sanic, orm_modules: dict):
    # register redis
    redis.register(app)
    scheduler.register(app)

    # register bot service
    peon_bot.register_bot(app, orm_modules)