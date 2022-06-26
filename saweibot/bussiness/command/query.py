import asyncio
from time import sleep
from sanic.log import logger


from saweibot.data.wrappers import BehaviorRecordWrapper
from saweibot.text import QUERY_SUCCESS_TIPS, QUERY_FAILED_TIPS
from ..helper import MessageHelepr

async def query_user(*params, helper: MessageHelepr):
    
    # check user has permission.
    if not (await helper.is_group_admin()) and not (await helper.is_whitelist_user()):
        return

    params_count = len(params)
    if params_count == 1:
        target_id = params[0]

        if target_id is None:
            return 

        # get chat member
        try :
            member = await helper.bot.get_chat_member(helper.chat_id, target_id)
            # send user's metion.
            await helper.bot.send_message(QUERY_SUCCESS_TIPS.format(full_name=member.user.full_name,
                                                                user_id=member.user.id))
            logger.info(f"User {helper.user.full_name} query member_id {target_id}")
        except Exception as _e:
            await helper.bot.send_message(QUERY_FAILED_TIPS.format(user_id=member.user.id))
            logger.error(_e)

        