import os
import ujson
from urllib.parse import urljoin

from sanic import Sanic
from sanic.log import logger


from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentTypes

SERVICE_CODE = "peon_bot"

async def get_bot() -> Bot:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

async def get_dp() -> Dispatcher:
    app = Sanic.get_app()
    return getattr(app.ctx, f"{SERVICE_CODE}_dp")
    
async def setup(app: Sanic):
    bot = Bot(token=app.config.TGBOT_PEON_TOKEN)
    dp = Dispatcher(bot)

    # define bot handle
    @dp.message_handler(content_types=ContentTypes.ANY | ContentTypes.ANIMATION | ContentTypes.AUDIO | ContentTypes.STICKER)
    async def on_message(message: Message):
        Bot.set_current(bot)
        await message.reply("test")
        bot.delete_message()
        await message.delete()
        print(message)


    hook_route = os.path.join("/tgbot/peon", app.config.TGBOT_PEON_TOKEN)
    webhook_uri = urljoin(app.config['DOMAIN_URL'], hook_route)
    await bot.set_webhook(webhook_uri)

    # Attach to ctx
    setattr(app.ctx, SERVICE_CODE, bot)
    setattr(app.ctx, f"{SERVICE_CODE}_dp", dp)
    logger.info(f"Register bot: {SERVICE_CODE}")