from saweibot.common import CommandMap

from .setpoint import set_reocrd_point
from .point import get_point
from .query import query_user
from .save import save_message

map = CommandMap(prefix='$')

map.register_command_handler("setpoint", set_reocrd_point)
map.register_command_handler("point", get_point)
map.register_command_handler("point", get_point)
map.register_command_handler("query", query_user)
map.register_command_handler("save", save_message)