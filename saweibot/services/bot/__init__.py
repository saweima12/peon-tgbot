from aiogram import Bot
from sanic import Sanic
from . import bot
from .bot import get_bot, get_dp, set_webhook, set_current

def register(app: Sanic) -> Bot:
    
    # setup bot
    instance = bot.setup(app)
    return instance
    