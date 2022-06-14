# coding=utf-8
from curses import wrapper
from sanic.log import logger
from aiogram import Bot
from aiogram.types import Message

from saweibot.storages.redis import RedisObjFactory

from .data.meta import SERVICE_CODE
from .data.wrappers.chat_message import ChatMessageWrapper
from .data.wrappers.chat_config import ChatConfigWrapper
from .helper import MessageHelepr
from .command import map as command_map

async def process_start_command(message: Message, bot: Bot):
    helper = MessageHelepr(SERVICE_CODE, message)

    # check user permission
    if not await helper.is_whitelist_user():
        return 

    # check target doesn't registed.
    if await helper.is_group_registered():
        await helper.msg.reply("The group has already register")
        return

    # chekc target is group.
    if helper.is_group():
        # register group chat.
        wrapper = ChatConfigWrapper(SERVICE_CODE, helper.chat_id)
        # set module.
        model = await wrapper.get_model()
        model.status = "ok"
        # add to redis.
        await wrapper.save_proxy(model)
        await helper.msg.reply("The group register finished.")
        logger.info(f"Register group - {helper.chat.full_name}")


async def process_stop_command(message: Message, bot:Bot):
    helper = MessageHelepr(SERVICE_CODE, message)

    # check user permission.
    in_whitelist = await helper.is_whitelist_user()
    is_group_admin = await helper.is_group_admin()

    if not in_whitelist and not is_group_admin:
        return

    # set config to disable
    if await helper.is_group_registered():
        wrapper = helper.chat_config_wrapper()
        await wrapper.proxy.set("ng", ".status")
        await message.reply("Deregister success.")
        
async def process_join_chat(message: Message, bot: Bot):
    logger.info("on join:", message.as_json())

async def process_chat_message(message: Message, bot: Bot):
    helper = MessageHelepr(SERVICE_CODE, message)
    
    if helper.is_group():
        await _process_group_msg(helper, bot)

    elif helper.is_private_chat():
        await _process_private_msg(helper, bot)

async def _process_group_msg(helper: MessageHelepr, bot: Bot):

    # check chat_id in whitelist.
    if not await helper.is_group_registered() :
        return

    # custom command handle
    if helper.is_text():
        if command_map.is_avaliable(helper.content):
            await command_map.notify(helper.content, helper=helper)
    # print(await helper.is_group_admin())
    # print(message)
    # check message rule.
    # write into msg buffer.
    wrapper = await helper.chat_message_wrapper()
    await wrapper.append(helper.message_model)


async def _process_private_msg(helper: MessageHelepr, bot: Bot):
    pass