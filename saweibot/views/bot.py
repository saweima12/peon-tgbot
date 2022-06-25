from sanic import HTTPResponse, Request, Blueprint, response, text
from sanic.log import logger
from aiogram.types import Update


from saweibot.services import bot

bp = Blueprint("peon_bot", url_prefix="/peon")

@bp.get("/")
async def me(request: Request) -> HTTPResponse:
    """
    PeonBot Index

    :param reuqest [sanic.Request]
    """
    _bot = bot.get_bot()
    me = await _bot.get_me()

    return text(me.as_json())


@bp.post("/<token:str>")
async def peon(request: Request, token: str) -> HTTPResponse:
    """
    PeonBot Webhook

    :param reuqest [sanic.Reqeust]
    :param token [str] -> Telegram.bot_token
    """
    # check token is correct.
    _bot = bot.get_bot()
    if _bot._token != token:
        return response.empty(status=404)

    # dispatch update event.
    _dp = bot.get_dp()

    # set currenct bot.
    bot.set_current()

    logger.debug(f"Update: {request.json}")    

    _update = Update(**request.json)
    try:
        await _dp.process_update(_update)
        return response.empty(status=200)
    except Exception as _e:
        logger.error(_e)

    return response.empty(status=400)

