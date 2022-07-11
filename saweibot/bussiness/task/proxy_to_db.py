from datetime import timedelta
from saweibot.data.wrappers.behavior_record import BehaviorRecordWrapper
from saweibot.services.scheduler.struct import AppScheduler

from saweibot.data.entities import PeonChatConfig
from saweibot.data.wrappers.chat_config import ChatConfigWrapper
from saweibot.meta import SERVICE_CODE
from saweibot.data.wrappers import UserWhitelistWrapper, ChatWatcherUserWrapper, ChatUrlBlackListWrapper

def register_task(scheduler: AppScheduler):

    @scheduler.register_task("proxy_to_db", timedelta(minutes=10))
    async def proxy_to_db_task():      
        # save user whitelist.
        whitelist_wrapper = UserWhitelistWrapper(SERVICE_CODE)
        whitelist_model = await whitelist_wrapper.get_model()
        await whitelist_wrapper.save_db(whitelist_model)
        
        # loading all chat data.
        chats = await PeonChatConfig.filter(status="ok")

        for chat in chats:
            # save chat config.
            config_wrapper = ChatConfigWrapper(SERVICE_CODE, chat.chat_id)
            config = await config_wrapper.get_model()
            await config_wrapper.save_db(config)

            # save behavior record.
            behavior_wrapper = BehaviorRecordWrapper(SERVICE_CODE, chat.chat_id)
            await behavior_wrapper.save_all_db()
            await behavior_wrapper.delete_proxy() # save finished, remove record map.

            # save url blacklist
            url_blacklist_wrapper = ChatUrlBlackListWrapper(SERVICE_CODE, chat.chat_id)
            url_blacklist = await url_blacklist_wrapper.get_model()
            await url_blacklist_wrapper.save_db(url_blacklist)