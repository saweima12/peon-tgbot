from enum import unique
from attr import field
from tortoise import fields
from tortoise.models import Model

class BotChatWhitelist(Model):
    bot_id = fields.CharField(max_length=20, index=True)
    chat_id = fields.BigIntField(index=True)
    status = fields.CharField(max_length=8)
    created_date = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "bot_chat_whitelist"