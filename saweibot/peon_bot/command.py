import asyncio
from saweibot.core import CommandMap
from saweibot.utils import parse_int

from .helper import MessageHelepr


map = CommandMap(prefix='$')

@map.register_command('rmall')
async def remove_msg_by_user(*params, helper: MessageHelepr):
    
    # must be reply a target.
    if not helper.reply_msg:
        return 
    # check user has permission.
    if not (await helper.is_group_admin()) and not (await helper.is_whitelist_user()):
        return

    # process reply message.  
    reply_helper = MessageHelepr(helper.bot_id, helper.reply_msg)

    # get message list from buffer
    chat_msg_wrapper = await helper.chat_message_wrapper()
    deleted_wrapper = helper.deleted_message_wrapper()
    msg_list = [ item for item in await chat_msg_wrapper.list() if item.user_id == reply_helper.user_id]
    deleted_keys = await deleted_wrapper.keys()

    async def delete_msg(msg):
        # check msg has been deleted?
        if msg.message_id in deleted_keys:
            return
        # try to delete message.
        try:
            await deleted_wrapper.append(msg.message_id, msg.json())
            await helper.chat.delete_message(msg.message_id)
            print("add list:", msg.message_id)
        except Exception as _e:
            print(msg.message_id)
            print(_e)

    tasks = []        

    for msg in msg_list:
        tasks.append(delete_msg(msg))

        if len(tasks) >= 10:
            await asyncio.gather(*tasks)
            tasks = []
            await asyncio.sleep(1.0)
    print("weeed")
    await asyncio.gather(*tasks)