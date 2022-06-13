# coding=utf-8
from sanic.log import logger
from aiogram import Bot
from aiogram.types import Message

from saweibot.storages.redis import RedisObjFactory

from .data.meta import SERVICE_CODE
from .data.wrappers.chat_message import ChatMessageWrapper
from .data.wrappers.chat_config import ChatConfigWrapper
from .helper import MessageHelepr

async def process_start_command(message: Message, bot: Bot):
    helper = MessageHelepr(SERVICE_CODE, message)

    if not await helper.is_whitelist_user():
        return 

    if await helper.is_group_registed():
        await helper.msg.reply("The group has already register")
        return

    if helper.is_group:
        # register group chat.
        wrapper = ChatConfigWrapper(SERVICE_CODE, helper.chat_id)
        await wrapper.save_proxy()
        await helper.msg.reply("The group register finished.")
        logger.info(f"Register group - {helper.chat.full_name}")


async def process_join_chat(message: Message, bot: Bot):
    logger.info("on join:", message.as_json())

async def process_chat_message(message: Message, bot: Bot):
    helper = MessageHelepr(SERVICE_CODE, message)
    
    if helper.is_group:
        await _process_group_msg(helper, bot)

    elif helper.is_private_chat:
        await _process_private_msg(helper, bot)

async def _process_group_msg(helper: MessageHelepr, bot: Bot):

    # check chat_id in whitelist.
    if not await helper.is_group_registed():
        return

    # custom command handle
    print("weed")

    # print(message)
    # check message rule.
    # write into msg buffer.
    buffer = RedisObjFactory(prefix=SERVICE_CODE).get_circular_buffer(40, "prog")
    await buffer.append(helper.content.as_json())

async def _process_private_msg(helper: MessageHelepr, bot: Bot):
    pass