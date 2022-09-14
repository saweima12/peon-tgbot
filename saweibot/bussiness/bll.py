# coding=utf-8
from datetime import timedelta
import re
import asyncio
from typing import List
from sanic.log import logger
from aiogram.types import Message

from saweibot.meta import SERVICE_CODE
from saweibot.services import opencc
from saweibot.data.entities import PeonChatConfig
from saweibot.data.models import ChatBehaviorRecordModel

from .command import map as command_map
from .helper import MessageHelepr
from .operate import PermissionLevel, set_media_permission, record_deleted_message

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
    
    ng_point = 0
    # check message.
    if _member.status != "ok":
        ng_point = await _get_ng_point(helper, _record)
    
    # process task
    _tasks = []

    # add delete task 
    if ng_point >= 2:
        _tasks.append(helper.msg.delete())
        _tasks.append(record_deleted_message(helper.chat_id, helper.msg))
        logger.info(f"Remove user {helper.user.full_name}'s message: {helper.message_model.dict()}")

        if _record.msg_count > 0:
            _member.ng_count += 1

    # execute set_permission task.
    if (len(_tasks) > 0 or _record.msg_count < 1):
        if _member.ng_count >= 3:
            _delta = timedelta(minutes=30) * _member.ng_count
            _tasks.append(set_media_permission(helper.bot, helper.chat_id, helper.user_id, PermissionLevel.CURB,  _delta))
        else:
            _tasks.append(set_media_permission(helper.bot, helper.chat_id, helper.user_id, PermissionLevel.LIMIT))


        await asyncio.gather(*_tasks)

    if not helper.is_text() or helper.is_forward():
        return 

    if not len(helper.msg.text) >= 2:
        return

    # increase message counter & ng_count
    _record.full_name = helper.user.full_name
    _record.msg_count += 1
    await asyncio.gather(
        behavior_wrapper.set(helper.user_id, _record),
        watcher_wrapper.set(helper.user_id, _member)
    )

async def _get_ng_point(helper: MessageHelepr, record: ChatBehaviorRecordModel) -> int:

    if await helper.is_group_admin():
        return 0

    point = 0
    # check message type & content allow ?
    config = await helper.chat_config_wrapper().get_model()

    if helper.is_forward():
        # check is forward message ?.
        if not check_forward_allow(helper, config.allow_forward):
            point += 2
    else:
        # check content.
        url_blacklist = await helper.url_blacklist_wrapper().get_model()
        if not check_content_allow(helper, url_blacklist.pattern_list):
            point += 2 

    # check user name.
    if not check_username_allow(helper, config.block_name_keywords):
        point += 1

    # check message length.
    if helper.is_text():
        if len(helper.msg.text) < 3:
            point +=1

    return point

def check_username_allow(helper: MessageHelepr, keywords: List[str] = []) -> bool:

    if not keywords:
        return True

    # extract all chinese_keyword.
    c_str = "".join(re.findall(r"([\u4E00-\u9FFF]+)", helper.user.full_name))
    # converter
    converter = opencc.get()
    tc_str = converter.convert(c_str)

    # create ptn
    temp = "|".join(keywords)
    ptn = f"((?:{temp}))"

    # match keyword
    result = re.findall(ptn, tc_str)

    if result:
        return False

    return True


def check_forward_allow(helper: MessageHelepr, allow_list: List[str] = []) -> bool:
     # check channel id is allow ?
    from_chat = helper.msg.forward_from_chat

    if from_chat:
        from_id = str(from_chat.id)

        if from_id == helper.chat_id:
            return True

        if from_id in allow_list:
            return True

    return False
    
def check_content_allow(helper: MessageHelepr, block_url_list: List[str] = []) -> bool:

    # user isn't admin and content is not text, delete it.
    if not helper.is_text():
        return False

    if helper.msg.via_bot:
        return False
    
    if helper.get_custom_emoji():
        return False

    if helper.get_mentions():
        return False

    if helper.has_url():
        # get entities url from message.
        urls = [ entity.get_text(helper.msg.text) for entity in helper.msg.entities if entity.type == "url"]
        
        # check pattern & url
        for pattern in block_url_list:
            _ptn = r".+({}).+".format(pattern)
            for url in urls:
                if re.match(_ptn, url):
                    return False

    return True