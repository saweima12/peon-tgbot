import datetime as dt
from sanic import HTTPResponse, Request, Blueprint, response, text
from sanic.log import logger
from aiogram.types import Update

from saweibot.meta import SERVICE_CODE
from saweibot.text import DELETED_COUNT_TIPS, DELETED_PAGE
from saweibot.data.entities import ChatDeletedMessage, PeonChatConfig, ChatBehaviorRecord, ChatWatchUser
from saweibot.data.wrappers import ChatConfigWrapper
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
    # set currenct bot.
    _bot = bot.get_bot()
    bot.set_current(_bot)
    # check token is correct.
    if _bot._token != token:
        return response.empty(status=404)
    # get event dispatcher
    _dp = bot.get_dp()
    logger.debug(f"Update: {request.json}")
    _update = Update(**request.json)

    # get session
    session = await _bot.get_session()
    try:
        await _dp.process_update(_update)
        await session.close()
        return response.empty(status=200)
    except Exception as _e:
        logger.error(_e)
        await session.close()
        return response.empty(status=200)



@bp.get("/<token:str>/send_deleted")
async def send_deleted_tips(request: Request, token: str):
    
    # get deleted message
    _bot = bot.get_bot()
    if _bot._token != token:
        return response.empty(status=404)

    chats = await PeonChatConfig.filter(status="ok")

    # define datetime parameter.
    now = dt.datetime.combine(dt.datetime.utcnow(), dt.time(15, 0))
    start_time = now - dt.timedelta(days=1)
    check_time = now - dt.timedelta(days=14)

    # get bot clientsession.
    session = await _bot.get_session()

    for chat in chats:
        # get chat's deleted message.
        chat_id = chat.chat_id
        msg_count = await ChatDeletedMessage.filter(chat_id=chat_id, record_date__gte=start_time).count()
        
        # get config
        config_wrapper = ChatConfigWrapper(SERVICE_CODE, chat_id)
        config = await config_wrapper.get_model()
        
        # combine message
        _page_url = DELETED_PAGE.format(chat_id=chat_id)
        _text = DELETED_COUNT_TIPS.format(count=str(msg_count), url=_page_url)

        # send message.
        await _bot.send_message(chat_id, _text, parse_mode='Markdown')
        
        # find need to delete record
        checked_record = await ChatBehaviorRecord.filter(chat_id=chat_id, 
                                                        update_time__lte=check_time,
                                                        msg_count__lte=config.check_lowest_count)
        need_delete_user_list = [ record.user_id for record in checked_record ]
        if need_delete_user_list:
            await ChatBehaviorRecord.filter(chat_id=chat_id, user_id__in=need_delete_user_list).delete()
            await ChatWatchUser.filter(chat_id=chat_id, user_id__in=need_delete_user_list).delete()

        # delete older than 14 deleted_message
        await ChatDeletedMessage.filter(chat_id=chat_id, record_date__lte=check_time).delete()

        

    await session.close()

    return response.empty(200)