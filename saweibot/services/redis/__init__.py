from sanic import Sanic

from . import db
from .db import get_db

def register(app: Sanic):

    @app.before_server_start
    async def startup(app: Sanic, _):
        await db.setup(app)

    @app.before_server_stop
    async def dispose(app: Sanic, _):
        await db.dispose(app)