from attr import field
from tortoise import fields
from tortoise.models import Model

class ChatGroup(Model):
    table = "chat_group"
    chat_id = fields.IntField()
    chat_name = fields.CharField(max_length=40)

class ChatGroupPermission(Model):
    table = "chat_group_permission"
    chat_id = fields.IntField()
    user_id = fields.IntField()
    status = fields.CharField(max_length=5)
    update_date = fields.DatetimeField(auto_now=True)
