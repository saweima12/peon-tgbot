import asyncio
from sanic.log import logger

from ..helper import MessageHelepr
from . import CommandMap


async def remove_msg_by_user(*params, helper: MessageHelepr):
    
    # must be reply a target.
    if not helper.reply_msg:
        logger.debug("Must be reply a message.")
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

    # Define Task
    async def delete_msg(msg):
        # check msg has been deleted?
        if msg.message_id in deleted_keys:
            return
        # try to delete message.
        try:
            await deleted_wrapper.append(msg.message_id, msg)
            await helper.chat.delete_message(msg.message_id)
        except Exception as _e:
            logger.error(_e)

    _range = 10
    freq = len(msg_list) // _range
    
    for num in range(0, freq + 1):
        #  get slice range
        tasks = []
        start = num * _range
        end = (num + 1) * _range
        # batch process delete.
        for msg in msg_list[start:end]:
            tasks.append(delete_msg(msg))

        await asyncio.gather(*tasks)
