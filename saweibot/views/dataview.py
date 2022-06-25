from sanic import Blueprint, Request, response
from saweibot.data.entities import PeonChatConfig, ChatBehaviorRecord, ChatDeletedMessage

bp = Blueprint("dataview", url_prefix="/dataview")

@bp.get("/avaliable_chat")
async def get_avaliable_chat(request: Request):
    chats = await PeonChatConfig.filter(status="ok")
    

    return response.json(chats)


@bp.get("/member_point")
async def get_member_point(request: Request):
    pass


@bp.get("/delete_messages")
async def get_deleted_message(request: Request):
    pass