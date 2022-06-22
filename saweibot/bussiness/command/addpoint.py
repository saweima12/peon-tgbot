import re
from saweibot.text import ADD_POINT, NEED_REPLY_MESSAGE
from saweibot.utils.type_helper import parse_int

from ..helper import MessageHelepr


async def add_record_point(*params, helper: MessageHelepr):

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
        
        print(params, _num)
        # if first param not a number
        if _num is None:
            return

        if not helper.reply_msg:
            await helper.msg.reply(NEED_REPLY_MESSAGE)
            return 

        #  add point
        target_id = helper.reply_msg.from_user.id
        wrapper = helper.behavior_wrapper()
        _model = await wrapper.get(target_id)
        _model.msg_count += _num
        await wrapper.set(target_id, _model)
        await helper.msg.reply(ADD_POINT.format(user=helper.reply_msg.from_user.full_name,
                                                point=_model.msg_count))
    
    elif params_count >= 2:
        # has three above parameter. multiple mode.
        users = params[1:]
        print(users)

    else:
        return