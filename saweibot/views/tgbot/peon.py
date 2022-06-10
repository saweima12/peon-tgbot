from sys import prefix
import ujson
from sanic import Sanic, Request, Blueprint, response, text
from aiogram.types import Update

from saweibot.bots import peon_bot

bp = Blueprint("tgbot", url_prefix="/peon")


@bp.get("/")
async def me(request: Request):
    """
    PeonBot Index

    :param reuqest [sanic.Request]
    """
    bot = peon_bot.get_bot()
    me = await bot.get_me()

    return text(me.as_json())


@bp.post("/<token:str>")
async def peon(request: Request, token: str):
    """
    PeonBot Webhook

    :param reuqest [sanic.Reqeust]
    :param token [str] -> Telegram.bot_token
    """
    dp = peon_bot.get_dp()
    _update = Update(**request.json)
    try:
        await dp.process_updates([_update])
        return response.empty(status=200)
    except Exception as _e:
        print(_e)

    return response.empty(status=400)