from sanic import Sanic
from .peon_bot import setup as peon_setup

async def register_bots(app: Sanic):
    await peon_setup(app)
