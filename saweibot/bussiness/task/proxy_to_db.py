from datetime import timedelta
from saweibot.data.wrappers.behavior_record import BehaviorRecordWrapper
from saweibot.services.scheduler.struct import AppScheduler

from saweibot.data.entities import PeonChatConfig
from saweibot.data.wrappers.chat_config import ChatConfigWrapper
from saweibot.meta import SERVICE_CODE
from saweibot.data.wrappers import BotConfigWrapper, UserWhitelistWrapper, ChatWatcherUserWrapper

def register_task(scheduler: AppScheduler):

    @scheduler.register_task("proxy_to_db", timedelta(minutes=10))
    async def proxy_to_db_task():
        # save bot config
        bot_wrapper = BotConfigWrapper(SERVICE_CODE)
        bot_config = await bot_wrapper.get_model()
        await bot_wrapper.save_db(bot_config)
        
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