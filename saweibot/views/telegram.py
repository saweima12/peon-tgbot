import ujson
from sanic import Request, Blueprint, text
from telebot.types import Update

from saweibot.bots import peon_bot

bp = Blueprint("telegram")



@bp.post("/peon")
async def peon(request: Request):
    """
    
    """
    json_str = ujson.dumps(request.load_json())
    bot = await peon_bot.get_bot()
    

    return text('')