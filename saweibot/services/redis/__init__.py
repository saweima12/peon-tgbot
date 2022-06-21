from sanic import Sanic
from redis.asyncio import Redis

# export function.
from . import db
from .db import get

def register(app: Sanic) -> Redis:

    _redis = db.setup(app)

    @app.before_server_stop
    async def dispose(app: Sanic, _):
        await db.dispose(app)

    return _redis