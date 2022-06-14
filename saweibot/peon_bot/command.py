from aiogram import Bot
from saweibot.core.command import CommandMap
from saweibot.peon_bot.helper import MessageHelepr

map = CommandMap(prefix='$')

@map.register_command('rma')
async def remove_msg_by_user(*params, helper: MessageHelepr):
    # get parameter.
    if not helper.reply:
        return 
