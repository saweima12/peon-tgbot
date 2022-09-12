import asyncio
from saweibot.meta import SERVICE_CODE
from saweibot.data.entities import PeonChatConfig
from saweibot.data.wrappers import ChatConfigWrapper
from saweibot.services.scheduler import AppScheduler

def register_task(scheduler: AppScheduler):

    @scheduler.register_task("load_config")
    async def load_config_task():

        chats = await PeonChatConfig.filter(status="ok")

        _tasks = []
        for chat in chats:
            chat_id = chat.chat_id
            _tasks.append(ChatConfigWrapper(SERVICE_CODE, chat_id).get_model())

        await asyncio.gather(*_tasks)