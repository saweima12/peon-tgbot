from datetime import timedelta
from sanic.log import logger
from saweibot.services.bot import get_bot
from saweibot.data.wrappers.behavior_record import BehaviorRecordWrapper
from saweibot.meta import SERVICE_CODE
from saweibot.services.scheduler.struct import AppScheduler

from saweibot.data.entities import PeonChatConfig
from saweibot.data.wrappers.chat_config import ChatConfigWrapper

def register_task(scheduler: AppScheduler):

    @scheduler.register_task("cache_admin", timedelta(minutes=10))
    async def cache_admin_task():
        #
        chats = await PeonChatConfig.filter(status="ok")

        bot = get_bot()
        session = await bot.get_session()
        try:
            for chat in chats:

                admin_list = await bot.get_chat_administrators(chat.chat_id)


                admin_id_set = set([str(item.user.id) for item in admin_list])
                config_wrapper =  ChatConfigWrapper(SERVICE_CODE, chat.chat_id)

                _model = await config_wrapper.get_model()
                _model.adminstrators = list(admin_id_set)

                await config_wrapper.save_proxy(_model)            
        except Exception as _e:
            logger.error(_e)
        finally:
            await session.close()