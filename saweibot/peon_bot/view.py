from sanic import HTTPResponse, Request, Blueprint, response, text
from aiogram.types import Update

from .bot import get_bot, get_dp

bp = Blueprint("peon_bot", url_prefix="/peon")

@bp.get("/")
async def me(request: Request) -> HTTPResponse:
    """
    PeonBot Index

    :param reuqest [sanic.Request]
    """
    bot = get_bot()
    me = await bot.get_me()

    return text(me.as_json())

@bp.get("/test")
async def test(request: Request) -> HTTPResponse:
    return text('')


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