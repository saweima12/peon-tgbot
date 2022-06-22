from aiogram import Bot
from aiogram.types.chat_permissions import ChatPermissions

async def set_media_permission(bot: Bot, chat_id: str, user_id: str, is_open: bool):
    
    if is_open:
        permission = ChatPermissions(can_send_messages=True,
                                    can_send_media_messages=True,
                                    can_send_other_messages=True,
                                    can_add_web_page_previews=True)
    else:
        permission = ChatPermissions(can_send_messages=True,
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False)
    await bot.restrict_chat_member(chat_id, user_id, permission)
