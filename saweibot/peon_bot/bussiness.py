from asyncio.log import logger
from aiogram import Bot
from aiogram.types import Message

from saweibot.storages.redis import RedisObjFactory

from .data.meta import SERVICE_CODE
from .data.wrappers.chat_message import ChatMessageWrapper
from .data.wrappers.chat_config import ChatConfigWrapper
from .helper import MessageHelepr

async def process_start_command(message: Message, bot: Bot):
    print("on start:", message.as_json())
    helper = MessageHelepr(SERVICE_CODE, message)

    if not await helper.is_whitelist_user():
        return 

    if helper.is_chat_group:
        if await helper.is_chat_registed():
            await helper.msg.reply("The group has already register")
            return
            # register chat_id
        wrapper = ChatConfigWrapper(SERVICE_CODE, helper.chat_id)
        await wrapper.save_proxy()
        await helper.msg.reply("The group register finished.")
        return


async def process_join_chat(message: Message, bot: Bot):
    print("on join:", message.as_json())

async def process_chat_message(message: Message, bot: Bot):

    helper = MessageHelepr(SERVICE_CODE, message)
    if helper.is_chat_group:
        # group chat.
        await _process_group_msg(helper, bot)
        return

    await _process_private_msg(helper, bot)
    # 

async def _process_group_msg(helper: MessageHelepr, bot: Bot):

    if not await helper.is_chat_registed():
        return 

    # custom command handle
    # print(message)
    # check message rule.
    # write into msg buffer.
    # check chat_id in whitelist.
    buffer = RedisObjFactory(prefix=SERVICE_CODE).get_circular_buffer(40, )
    await buffer.append(helper.msg.as_json())




async def _process_private_msg(helper: MessageHelepr, bot: Bot):
    pass