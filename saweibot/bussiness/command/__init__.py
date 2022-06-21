from saweibot.common import CommandMap

from .rmall import remove_msg_by_user
from .addpoint import add_record_point
from .setpoint import set_reocrd_point
from .point import get_point

map = CommandMap(prefix='$')

map.register_command_handler("rmall", remove_msg_by_user)
map.register_command_handler("addpoint", add_record_point)
map.register_command_handler("setpoint", set_reocrd_point)
map.register_command_handler("point", get_point)