from datetime import datetime, timedelta
import traceback
from asyncio.log import logger
from sanic import Blueprint, Request, response
from saweibot.data.entities import PeonChatConfig, ChatBehaviorRecord, ChatDeletedMessage
from saweibot.data.schema import AvailableChatSchema, ChatMemberPointSchema, ChatDeleteMessageSchema

bp = Blueprint("dataview", url_prefix="/dataview")

@bp.get("/chats")
async def get_chats(request: Request):
    chats = await PeonChatConfig.filter(status="ok")
    _data = [AvailableChatSchema(
                    chat_id=chat.chat_id, 
                    full_name=chat.chat_name, 
                    config_json=chat.config_json
                ).dict() for chat in chats]

    return response.json(_data)

@bp.get('/chats/<id>')
async def get_chat_info(request: Request, id: str):
    chat = await PeonChatConfig.get_or_none(chat_id=id)

    if not chat:
        return response.empty(404)

    _data = AvailableChatSchema(
        chat_id=chat.chat_id,
        full_name=chat.chat_name,
        config_json=chat.config_json
    ).dict()
    return response.json(_data)


@bp.get("/member_point")
async def get_member_point(request: Request):
    chat_id = request.args.get("chat")

    if not chat_id:
        return response.empty(400)
    try:
        result = await ChatBehaviorRecord.filter(chat_id=chat_id)

        if not result:
            return response.empty(404)


        result = [ChatMemberPointSchema(
                        user_id=item.user_id, 
                        full_name=item.full_name,
                        point=item.msg_count,
                        last_updated=item.update_time.isoformat()
                    ).dict() for item in result]
        return response.json(result)
    except Exception:
        logger.error(traceback.format_exc())
        return response.text(traceback.format_exc(), 500)

@bp.get("/deleted_messages")
async def get_deleted_message(request: Request):
    chat_id = request.args.get("chat")

    if not chat_id:
        return response.empty(400)

    start = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d")

    try:
        print(chat_id)
        result = await ChatDeletedMessage.filter(chat_id=chat_id, record_date__gte=start)

        if not result:
            return response.empty(404)
        
        _result = []
        # process data
        for item in result:
            raw = item.message_json
            # remove field.
            _check_remove('chat', raw)
            _check_remove('sticker', raw)
            _check_remove('photo', raw)
            _check_remove('animation', raw)
            _check_remove('audio', raw)
            _check_remove('video', raw)
            _check_remove('voice', raw)
            
            _result.append(
                ChatDeleteMessageSchema(
                    content_type=item.content_type,
                    raw=raw,
                    record_time=item.record_date.isoformat()
                ).dict()
            )
            print(_result)
        
        return response.json(_result)
    except Exception:
        logger.error(traceback.format_exc())
        return response.empty(404)


def _check_remove(key: str, obj: dict):
    if key in obj:
        obj.pop(key)
    return obj