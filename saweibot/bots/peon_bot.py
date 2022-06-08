from sanic import Sanic
from telebot import TeleBot
from telebot.async_telebot import AsyncTeleBot

SERVICE_CODE = "peon_bot"

async def get_bot() -> TeleBot:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)
    
async def setup(app: Sanic):
    bot = AsyncTeleBot(token=app.config.BOT_TOKEN)


    # Define handle
    @bot.message_handler(commands=['test'])
    async def _test():
       test()

    # Attach to ctx
    setattr(app.ctx, SERVICE_CODE, bot)

def test():
    print("test")