import re
from sanic.log import logger
from saweibot.utils.type_helper import parse_int
from saweibot.text import NEED_REPLY_MESSAGE, SET_POINT

from ..helper import MessageHelepr


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

        #  set point
        target_id = helper.reply_msg.from_user.id
        wrapper = helper.behavior_wrapper()
        _model = await wrapper.get(target_id)
        _model.msg_count = _num
        await wrapper.set(target_id, _model)
        await helper.msg.reply(SET_POINT.format(user=helper.reply_msg.from_user.full_name, 
                                                point=_model.msg_count))
        logger.info(f"Administrator [{helper.user.full_name}] set [{helper.reply_msg.from_user.full_name}] point to {_num}")

    elif params_count >= 2:
        # has three above parameter. multiple mode.
        users = params[1:]
        print(users)

    else:
        return