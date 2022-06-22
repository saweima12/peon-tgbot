from datetime import timedelta
from sanic.log import logger
from aiogram.types.chat_permissions import ChatPermissions

from saweibot.bot import get_bot
from saweibot.data.entities import ChatWatchUser
from saweibot.data.wrappers import BehaviorRecordWrapper
from saweibot.data.wrappers.chat_config import ChatConfigWrapper
from saweibot.data.wrappers.watch_user import ChatWatcherUserWrapper
from saweibot.meta import SERVICE_CODE

from saweibot.services.scheduler.struct import AppScheduler

def register_task(scheduler: AppScheduler):

    @scheduler.register_task("check_watchlist", period=timedelta(minutes=2))
    async def check_watchlist_task():
        # get all watch member.
        watch_users = await ChatWatchUser.filter(status="ng")

        bot = get_bot()
        # traversal all watch user.
        for row in watch_users:
            behavior_wrapper = BehaviorRecordWrapper(SERVICE_CODE, row.chat_id)
            config_wrapper = ChatConfigWrapper(SERVICE_CODE, row.chat_id)
            watch_wrapper = ChatWatcherUserWrapper(SERVICE_CODE, row.chat_id)
            # get model
            config = await config_wrapper.get_model()
            record = await behavior_wrapper.get(row.user_id)
            watch_user = await watch_wrapper.get(row.user_id)

            if record.msg_count >= config.senior_count:
                # update reids
                watch_user.status = "ok" 
                await watch_wrapper.set(row.user_id, watch_user)
                # udpate database
                await watch_wrapper.save_db(row.user_id, watch_user)

                await bot.restrict_chat_member(row.chat_id, row.user_id, ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True
                ))

                logger.info(f"set {record.full_name} member permission")