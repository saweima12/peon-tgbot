import asyncio
from time import sleep
from sanic.log import logger


from saweibot.data.wrappers import BehaviorRecordWrapper
from saweibot.text import QUERY_SUCCESS_TIPS, QUERY_FAILED_TIPS, MEMBER_LINK
from ..helper import MessageHelepr

async def query_user(*params, helper: MessageHelepr):
    
    # check user has permission.
    if not (await helper.is_group_admin()) and not (await helper.is_whitelist_user()):
        return

    if len(params) < 1:
        return


    query_str= "".join(params)
    members_str = []

    # get chat's member data.
    for member_id in params:
        try:
            member = await helper.bot.get_chat_member(helper.chat_id, member_id)
            members_str.append(MEMBER_LINK.format(full_name=member.user.full_name, user_id=member.user.id))
        except Exception as _e:
            logger.info(f"User not found {member_id}")

    if not members_str:
        # query is empty
        _tips = await helper.bot.send_message(helper.chat_id, QUERY_FAILED_TIPS, parse_mode='Markdown')
        logger.info("Query failed, object not found.")
        return

    try :
        _content = "\n".join(members_str)
        # send user's metion.
        _msg = QUERY_SUCCESS_TIPS.format(content=_content, count=len(members_str))
        
        _tips = await helper.bot.send_message(helper.chat_id, _msg, parse_mode='Markdown')
        logger.info(f"User {helper.user.full_name} query member_id {query_str}")
    except Exception as _e:
        logger.error(_e)
