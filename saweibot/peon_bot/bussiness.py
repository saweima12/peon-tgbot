from aiogram import Bot
from aiogram.types import Message

from saweibot.storages.redis import RedisObjFactory

from .data.meta import SERVICE_CODE


async def process_start_command(message: Message, bot: Bot):
    print("on start:", message.as_json())

async def process_join_chat(message: Message, bot: Bot):
    print("on join:", message.as_json())

async def process_chat_message(message: Message, bot: Bot):
    # process parameter
    chat = message.chat

    # check chat_id in whitelist.
    buffer = RedisObjFactory(prefix=SERVICE_CODE).get_circular_buffer(40, "prog")
    await buffer.append(message.as_json())

    # custom command handle
    # print(message)

    # check message rule.

    # write into msg buffer.
