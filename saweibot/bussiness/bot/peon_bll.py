from aiogram import Bot
from aiogram.types import Message

from saweibot.bussiness import redis

async def process_start_command(message: Message, bot: Bot):
    pass

async def process_join_chat(message: Message, bot: Bot):
    pass

async def process_chat_message(message: Message, bot: Bot):

    # process parameter
    chat = message.chat

    # check chat_id in whitelist.
    
    # custom command handle
    _factory = redis.ContextFactory()

    # check message rule.
    chat.restrict()
    # write into msg buffer.
    _buffer = _factory.get_chatgroup_msgbuf(chat.id, 40)
    await _buffer.append(message.as_json())
