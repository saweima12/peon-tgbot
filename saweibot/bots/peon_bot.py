import os
import ujson
from urllib.parse import urljoin

from sanic import Sanic
from sanic.log import logger


from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentTypes

SERVICE_CODE = "peon_bot"
DP_CODE = f"{SERVICE_CODE}_dp"

async def get_bot() -> Bot:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

async def get_dp() -> Dispatcher:
    app = Sanic.get_app()
    return getattr(app.ctx, DP_CODE)

async def setup(app: Sanic):
    bot = Bot(token=app.config.TGBOT_PEON_TOKEN)
    dp = Dispatcher(bot)

    # define bot handle
    @dp.message_handler(content_types=ContentTypes.ANY | ContentTypes.ANIMATION | ContentTypes.AUDIO | ContentTypes.STICKER)
    async def on_message(message: Message):
        Bot.set_current(bot)
        await message.reply("test")
        await bot.delete_message(message.chat.id, message.message_id)
        print(message)


    hook_route = os.path.join("/tgbot/peon", app.config.TGBOT_PEON_TOKEN)
    webhook_uri = urljoin(app.config['DOMAIN_URL'], hook_route)
    await bot.set_webhook(webhook_uri)

    # Attach to ctx
    setattr(app.ctx, SERVICE_CODE, bot)
    setattr(app.ctx, DP_CODE, dp)
    logger.info(f"Register bot: {SERVICE_CODE}")
    logger.info(f"Register Dispatcher: {DP_CODE}")

async def dispose(app: Sanic):
    if hasattr(app.ctx, SERVICE_CODE):
        bot: Bot = getattr(app.ctx, SERVICE_CODE)
        await bot.delete_webhook()
        logger.info(f"Close Bot: {SERVICE_CODE}")

    if hasattr(app.ctx, DP_CODE):
        dp: Dispatcher = getattr(app.ctx, DP_CODE)
        await dp.reset_webhook()
        logger.info(f"Close Dispatcher: {DP_CODE}")
