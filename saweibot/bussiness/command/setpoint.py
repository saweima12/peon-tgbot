import re
from sanic.log import logger
from saweibot.utils.type_helper import parse_int
from saweibot.text import NEED_REPLY_MESSAGE, SET_POINT

from ..helper import MessageHelepr
from ..operate import set_media_permission

async def set_reocrd_point(*params, helper: MessageHelepr):

    # check user has permission.
    if not (await helper.is_group_admin()) and not (await helper.is_whitelist_user()):
        return

    # check parameters.
    params_count = len(params)
    if params_count < 1:
        return

    # only 2 parameter,  reply mode
    if params_count == 1:
        _num = parse_int(params[0])
        # if first param not a number
        if _num is None:
            return

        if not helper.reply_msg:
            await helper.msg.reply(NEED_REPLY_MESSAGE)
            return 

        # get wrapper
        behavior_wrapper = helper.behavior_wrapper()
        config_wrapper = helper.chat_config_wrapper()

        config = await config_wrapper.get_model()
        #  set point to proxy & database.
        target_msg = helper.reply_msg.from_user
        target_id = target_msg.id
        record = await behavior_wrapper.get(target_id)
        record.msg_count = _num
        await behavior_wrapper.set(target_id, record)

        watcher_wrapper = helper.watcher_wrapper()
        member = await watcher_wrapper.get(target_id, target_msg.full_name)
        # set watcher state.
        if record.msg_count >= config.senior_count:
            member.status = "ok"

            await set_media_permission(helper.bot, helper.chat_id, target_id, True)
            logger.info(f"Point over than {config.senior_count}, open sticker permission.")
        else:
            member.status = "ng"
            await set_media_permission(helper.bot, helper.chat_id, target_id, True)
            logger.info(f"Point lower than {config.senior_count}, close sticker permission.")


        await watcher_wrapper.set(target_id, member)
        await watcher_wrapper.save_db(target_id, member)
        await helper.bot.send_message(helper.chat_id, 
                                    SET_POINT.format(user=helper.reply_msg.from_user.full_name, 
                                                     point=record.msg_count))
        logger.info(f"Administrator [{helper.user.full_name}] set [{helper.reply_msg.from_user.full_name}] point to {_num}")

    elif params_count >= 2:
        # has three above parameter. multiple mode.
        users = params[1:]
        print(users)

    else:
        return