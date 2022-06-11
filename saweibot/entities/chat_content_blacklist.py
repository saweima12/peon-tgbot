from tortoise import fields
from tortoise.models import Model

class ChatContentBlacklist(Model):
    
    chat_id = fields.BigIntField(index=True)
    content_type = fields.CharField(max_length=100)
    file_id = fields.TextField()
    file_unique_id = fields.TextField()
    status = fields.CharField(max_length=8)

    class Meta:
        table = "chat_content_blacklist"