from datetime import datetime, timedelta
import traceback
from asyncio.log import logger
from sanic import Blueprint, Request, response
from saweibot.data.entities import PeonChatConfig, ChatBehaviorRecord, ChatDeletedMessage
from saweibot.data.schema import AvailableChatSchema, ChatMemberPointSchema, ChatDeleteMessageSchema

bp = Blueprint("dataview", url_prefix="/dataview")

@bp.get("/avaliable_chat")
async def get_avaliable_chat(request: Request):
    chats = await PeonChatConfig.filter(status="ok")
    _data = [AvailableChatSchema(
                    chat_id=chat.chat_id, 
                    full_name=chat.chat_name, 
                    config_json=chat.config_json
                ).dict() for chat in chats]

    return response.json(_data)


@bp.get("/member_point")
async def get_member_point(request: Request):
    chat_id = request.args.get("chat")

    if not chat_id:
        return response.json([])
    try:
        result = await ChatBehaviorRecord.filter(chat_id=chat_id)
        result = [ChatMemberPointSchema(
                        user_id=item.user_id, 
                        full_name=item.full_name,
                        point=item.msg_count,
                        last_updated=item.update_time.isoformat()
                    ).dict() for item in result]
        return response.json(result)
    except Exception:
        logger.error(traceback.format_exc())
        return response.json([])

@bp.get("/deleted_messages")
async def get_deleted_message(request: Request):
    chat_id = request.args.get("chat")

    if not chat_id:
        return response.json([])

    start = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d")

    try:
        result = await ChatDeletedMessage.filter(chat_id=chat_id, record_date__gte=start)
        if not result:
            return response.json([])
        
        result = [ChatDeleteMessageSchema(
                        content_type=item.content_type,
                        raw=item.message_json,
                        record_time=item.record_date.isoformat()
                    ).dict() for item in result]

        
        return response.json(result)
    except Exception:
        logger.error(traceback.format_exc())
        return response.json([])