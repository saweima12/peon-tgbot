import datetime as dt
from sanic import HTTPResponse, Request, Blueprint, response, text
from sanic.log import logger
from aiogram.types import Update

from saweibot.text import DELETED_COUNT_TIPS, DELETED_PAGE
from saweibot.data.entities import ChatDeletedMessage, PeonChatConfig
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

    session = await _bot.get_session()

    # dispatch update event.
    _dp = bot.get_dp()

    # set currenct bot.
    bot.set_current()

    logger.debug(f"Update: {request.json}")    

    _update = Update(**request.json)

    try:
        await _dp.process_update(_update)
        await session.close()
        return response.empty(status=200)
    except Exception as _e:
        logger.error(_e)
        await session.close()
        return response.empty(status=400)


@bp.get("/<token:str>/send_deleted")
async def send_deleted_tips(request: Request, token: str):
    
    # get deleted message
    _bot = bot.get_bot()
    if _bot._token != token:
        return response.empty(status=404)

    chats = await PeonChatConfig.filter(status="ok")

    now = dt.datetime.combine(dt.datetime.utcnow(), dt.time(15, 0))
    start = now - dt.timedelta(days=1)

    session = await _bot.get_session()
    for chat in chats:

        chat_id = chat.chat_id

        msg_count = await ChatDeletedMessage.filter(chat_id=chat_id, record_date__gte=start).count()
        
        _page_url = DELETED_PAGE.format(chat_id=chat_id)
        _text = DELETED_COUNT_TIPS.format(count=str(msg_count), url=_page_url)
        await _bot.send_message(chat_id, _text, parse_mode='Markdown')
    

    await session.close()
    return response.empty(200)