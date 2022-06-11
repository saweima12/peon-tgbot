from tortoise import fields
from tortoise.models import Model

class ChatBehaviorRecord(Model):
    chat_id = fields.BigIntField(index=True)
    user_id = fields.BigIntField(index=True)
    counter = fields.IntField()

    class Meta:
        table = "chat_behavior_record"