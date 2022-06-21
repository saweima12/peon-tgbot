from saweibot.common import CommandMap

from .setpoint import set_reocrd_point
from .point import get_point

map = CommandMap(prefix='$')

map.register_command_handler("setpoint", set_reocrd_point)
map.register_command_handler("point", get_point)