from textwrap import wrap
from sanic import HTTPResponse, Sanic, Request, Blueprint, response, text
from aiogram.types import Update

from saweibot.peon_bot.data.wrappers.bot_whitelist import ChatWhitelistWrapper

from .bot import get_bot, get_dp
from .data.meta import SERVICE_CODE
from .data.models import BotConfigModel
from .data.wrappers.bot_confg import BotConfigWrapper

bp = Blueprint("peon_bot", url_prefix="/peon")

@bp.get("/")
async def me(request: Request) -> HTTPResponse:
    """
    PeonBot Index

    :param reuqest [sanic.Request]
    """
    bot = get_bot()
    me = await bot.get_me()

    wrapper = ChatWhitelistWrapper(SERVICE_CODE)
    # bot_config: BotConfigModel = await wrapper.get_model()
    model = await wrapper.get_model()

    await wrapper.save_db()

    return text(model.json())


@bp.post("/<token:str>")
async def peon(request: Request, token: str) -> HTTPResponse:
    """
    PeonBot Webhook

    :param reuqest [sanic.Reqeust]
    :param token [str] -> Telegram.bot_token
    """
    # check token is correct.
    bot = get_bot()

    if bot._token != token:
        return response.empty(status=404)

    # dispatch update event.
    dp = get_dp()
    _update = Update(**request.json)
    try:
        await dp.process_update(_update)
        return response.empty(status=200)
    except Exception as _e:
        print(_e)

    return response.empty(status=400)