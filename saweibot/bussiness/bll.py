# coding=utf-8
import re
import asyncio
from sanic.log import logger
from aiogram.types import Message

from saweibot.data.entities import PeonChatConfig
from saweibot.data.models import ChatBehaviorRecordModel
from saweibot.meta import SERVICE_CODE
from saweibot.text import FIRST_URL_TIPS, MEDIA_MESSAGE_TIPS

from .command import map as command_map
from .helper import MessageHelepr
from .operate import set_media_permission, record_deleted_message

async def process_start_command(message: Message):
    helper = MessageHelepr(SERVICE_CODE, message)

    # must be group.
    if not helper.is_super_group():
        return

    is_group_registered = await helper.is_group_registered()
    is_whitelist_user = await helper.is_whitelist_user()
    # check group is registered or user is whitelist user.
    if (not is_group_registered) and (not is_whitelist_user):
        return 

    is_group_admin = await helper.is_group_admin()
    if not is_group_admin and not is_whitelist_user:
        return

    # register group chat.
    wrapper = helper.chat_config_wrapper()
    # set module.
    config = await wrapper.get_model()
    config.status = "ok"
    # add to redis.
    await wrapper.save_proxy(config)

    # write to database
    _default = {
        'status': 'ok',
        'chat_name': helper.chat.full_name,
        'config_json': config.dict()
    }
    await PeonChatConfig.update_or_create(_default,
                                        chat_id=helper.chat_id)
    await message.reply(f"Set bot active on {helper.chat.full_name} group.")
    logger.info(f"Set bot active on {helper.chat_id} group.")


async def process_stop_command(message: Message):
    helper = MessageHelepr(SERVICE_CODE, message)

    if not helper.is_super_group():
        return

    # set config to disable
    if not await helper.is_group_registered():
        return 

    # check user permission.
    in_whitelist = await helper.is_whitelist_user()
    is_group_admin = await helper.is_group_admin()

    if not in_whitelist and not is_group_admin:
        return
    
    # disable bot at taget gorup.
    wrapper = helper.chat_config_wrapper()
    await wrapper.proxy.set("ng", ".status")

    # write to database
    _update = { 'status': 'ng' }
    await PeonChatConfig.update_or_create(defaults=_update, chat_id=helper.chat_id)
    await message.reply(f"Set bot deactive on {helper.chat.full_name} group.")


async def process_chat_message(message: Message):
    helper = MessageHelepr(SERVICE_CODE, message)
    # set bot's context.
    try:
        if helper.is_super_group():
            await _process_group_msg(helper)
    except Exception as _e:
        logger.error("Process Error", message.as_json())
        raise _e

async def _process_group_msg(helper: MessageHelepr):
    # check chat_id in whitelist.
    if not await helper.is_group_registered() :
        return

    # custom command handle
    if helper.is_text():
        if command_map.is_avaliable(helper.content):
            await command_map.notify(helper.content, helper=helper)
            return

    # get watch user & record data..
    watcher_wrapper = helper.watcher_wrapper()
    _member = await watcher_wrapper.get(helper.user_id, helper.user.full_name)

    behavior_wrapper = helper.behavior_wrapper()
    _record = await behavior_wrapper.get(helper.user_id)
    

    need_delete = False
    # check message.
    if _member.status != "ok":
        need_delete = await _check_member_msg(helper, _record)
    
    # process task
    _tasks = []

    if need_delete:
        _tasks.append(helper.msg.delete())
        _tasks.append(record_deleted_message(helper.chat_id, helper.msg))
        logger.info(f"Remove user {helper.user.full_name}'s message: {helper.message_model.dict()}")

    if (len(_tasks) > 0 or _record.msg_count < 1) and not (await helper.is_group_admin()):
        _tasks.append(set_media_permission(helper.bot, helper.chat_id, helper.user_id, False))
        await asyncio.gather(*_tasks)

    if not helper.is_text() or helper.is_forward():
        return 

    if not len(helper.msg.text) >= 2:
        return

    # increase message counter
    _record.full_name = helper.user.full_name
    _record.msg_count += 1
    await behavior_wrapper.set(helper.user_id, _record)

async def _check_member_msg(helper: MessageHelepr, record: ChatBehaviorRecordModel):

    if await helper.is_group_admin():
        return False

    # user isn't admin and content is not text, delete it.
    if not helper.is_text() or helper.is_forward():
        return True

    # is first send message and has_url ?
    if helper.has_url():
        # get url blacklist wrapper.
        url_blacklist_wrapper = helper.url_blacklist_wrapper()

        if record.msg_count < 1:
            return True
        
        # get entities url from message.
        urls = [ entity.get_text(helper.msg.text) for entity in helper.msg.entities if entity.type == "url"]
        # get blacklist from proxy.
        _blacklist = await url_blacklist_wrapper.get_model()
        # check pattern & url
        for pattern in _blacklist.pattern_list:
            _ptn = r".+({}).+".format(pattern)
            for url in urls:
                if re.match(_ptn, url):
                    return True
    
    if helper.msg.via_bot:
        return True
    
    mentions = helper.get_mentions()
    ptn = r".+bot$"

    if mentions:
        for mention in mentions:
            _id = (mention.get_text(helper.msg.text))
            if re.match(ptn, _id, re.I):
                return True

    if helper.get_custom_emoji():
        return True

    return False
        
