from datetime import timedelta
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
                print("on update count", record.msg_count)
                watch_user.status = "ok" 
                await watch_wrapper.save_db(row.user_id, watch_user)
                # udpate database
                row.status = "ok"
                row.attach_json = watch_user.dict()
                await row.save()
