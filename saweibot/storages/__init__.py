from sanic import Sanic
from . import redis

def register(app: Sanic):
    
    @app.before_server_start
    async def setup(app, loop):
        await redis.setup(app)

    @app.before_server_stop
    async def dispose(app, loop):
        await redis.dispose(app)