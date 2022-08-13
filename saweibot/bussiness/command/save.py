from datetime import datetime
from saweibot.data.entities import ChatSavedMessage
from saweibot.text import SAVE_TIPS

from ..helper import MessageHelepr

async def save_message(*params, helper: MessageHelepr):
    # check user has permission.
    if not (await helper.is_group_admin()) and not (await helper.is_whitelist_user()):
        return

    if not helper.reply_msg:
        return

    reply_msg = helper.reply_msg

    await ChatSavedMessage.update_or_create(defaults={
        'message_json': reply_msg.to_python()
    }, message_id=reply_msg.message_id, chat_id=helper.chat_id)

    await helper.bot.send_message(helper.chat_id, SAVE_TIPS)