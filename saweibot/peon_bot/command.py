from saweibot.core import CommandMap

from .helper import MessageHelepr

map = CommandMap(prefix='$')

@map.register_command('rm')
async def remove_msg_by_user(*params, helper: MessageHelepr):
    # must be reply a target.
    if not helper.reply:
        return 
    
    # if doesn't has permission.
    if not (await helper.is_group_admin()) and not (await helper.is_whitelist_user()):
        return


