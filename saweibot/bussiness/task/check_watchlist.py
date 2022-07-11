import asyncio
from datetime import timedelta
from sanic.log import logger

from saweibot.services.bot import get_bot
from saweibot.data.entities import PeonChatConfig
from saweibot.data.models import ChatBehaviorRecordModel, ChatWatchUserModel
from saweibot.data.wrappers import BehaviorRecordWrapper
from saweibot.data.wrappers.chat_config import ChatConfigWrapper
from saweibot.data.wrappers.watch_user import ChatWatcherUserWrapper
from saweibot.meta import SERVICE_CODE

from saweibot.services.scheduler.struct import AppScheduler

from ..operate import set_media_permission

def register_task(scheduler: AppScheduler):

    @scheduler.register_task("check_watchlist", period=timedelta(minutes=5))
    async def check_watchlist_task():
        # get all watch chat.
        chats = await PeonChatConfig.filter(status="ok")
        bot = get_bot()

        for chat in chats:
            # traversal all watch group.
            behavior_wrapper = BehaviorRecordWrapper(SERVICE_CODE, chat.chat_id)
            config_wrapper = ChatConfigWrapper(SERVICE_CODE, chat.chat_id)
            watch_wrapper = ChatWatcherUserWrapper(SERVICE_CODE, chat.chat_id)

            # get chatConfig model & watch member id.
            config = await config_wrapper.get_model()
            watch_member_ids = await watch_wrapper.keys()

            async def update_member_status(member_id: str,
                                        data: ChatWatchUserModel, 
                                        record: ChatBehaviorRecordModel):
                # set redis & database.
                await watch_wrapper.set(member_id, data)
                await watch_wrapper.save_db(member_id, data)
                await behavior_wrapper.save_db(member_id, record)
                # post telegram api.
                if member_id in config.adminstrators:
                    return

                await set_media_permission(bot, chat.chat_id, member_id, True)
                logger.info(f"set [{record.full_name}]'s member permission")


            task_list = []
            _range = 10
            freq = len(watch_member_ids) // _range

            # process member
            for num in range(0, freq + 1):
                task_list = []
                start = num * _range
                end = (num + 1) * _range

                for member_id in watch_member_ids[start:end]:
                    # get member status.
                    watch_member = await watch_wrapper.get(member_id)

                    # Ignore members with a status of OK 
                    if watch_member.status == "ok":
                        continue
                    
                    # get member's behavior record
                    record = await behavior_wrapper.get(member_id)

                    if record.msg_count < config.senior_count:
                        continue
                    
                    # add task
                    watch_member.status = "ok"
                    task_list.append(update_member_status(member_id, watch_member, record))

                if task_list:
                    await asyncio.gather(*task_list)
            
            # task finished, remove watchlist.
            logger.debug("remove proxy.")
            await watch_wrapper.delete_proxy()
                