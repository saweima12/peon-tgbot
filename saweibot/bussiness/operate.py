from datetime import timedelta
from enum import Enum
from aiogram import Bot
from aiogram.types.message import Message
from aiogram.types.chat_permissions import ChatPermissions

from saweibot.data.entities import ChatDeletedMessage

class PermissionLevel:
    ALLOW = 0
    LIMIT = 1
    CURB = 2


async def set_media_permission(bot: Bot, chat_id: str, user_id: str, level: PermissionLevel, until_date: timedelta = None) -> bool:

    if level == PermissionLevel.ALLOW:
        permission = ChatPermissions(can_send_messages=True,
                                    can_send_media_messages=True,
                                    can_send_other_messages=True,
                                    can_add_web_page_previews=True)
    elif level == PermissionLevel.LIMIT:
        permission = ChatPermissions(can_send_messages=True,
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False)
    else:
        permission = ChatPermissions(can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False)

    result = await bot.restrict_chat_member(chat_id, user_id, permission, until_date=until_date)
    return result


async def record_deleted_message(chat_id: str, data: Message):
    
    content_type = "forward" if data.is_forward() else data.content_type

    _data = data.to_python()

    _data['full_name'] = data.from_user.full_name
    _data['content_type'] = data.content_type

    # write into database 
    await ChatDeletedMessage.create(chat_id=chat_id, 
                                content_type=content_type,
                                message_json=_data)
