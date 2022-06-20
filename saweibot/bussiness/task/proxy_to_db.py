from saweibot.data.entities import PeonChatConfig
from saweibot.data.wrappers.chat_config import ChatConfigWrapper
from saweibot.meta import SERVICE_CODE
from saweibot.data.wrappers import BotConfigWrapper

async def proxy_to_db_task():
    # loading all chat data.
    chats = PeonChatConfig.filter(chat_id="", status="ok")
    
    # get data from reids.


    # save bot conifg.

    # save user whitelist.

    # save chat config.

    # save watchlist

    # save behavior record.
    pass
