from sanic import Sanic
from . import peon_bot

async def register_bots(app: Sanic):
    await peon_bot.setup(app)

async def dispose_bots(app: Sanic):
    await peon_bot.dispose(app)