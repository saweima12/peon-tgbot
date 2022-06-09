from tortoise import fields
from tortoise.models import Model

class ChatMessage(Model):
    table = "chat_messages"
    message_id = fields.IntField(index=True)
    user_id = fields.IntField(index=True)
    chat_id = fields.BigIntField(index=True)
    content_type = fields.CharField(max_length=20)
    raw = fields.TextField()
    record_date = fields.DatetimeField(auto_now_add=True)