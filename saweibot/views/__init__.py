from sanic import Blueprint
from .tgbot.peon import bp as peon

tgbot = Blueprint.group([peon], url_prefix="/tgbot")