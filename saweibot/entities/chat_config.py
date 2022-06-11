from tortoise import fields
from tortoise.models import Model

class ChatConfig(Model):
    
    chat_id = fields.BigIntField(index=True)
    config_json = fields.JSONField()
    permission_json = fields.JSONField()

    class Meta:
        table = "chat_group"