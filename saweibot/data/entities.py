from attr import field
from tortoise import fields
from tortoise.models import Model


class PeonChatConfig(Model):
    
    chat_id = fields.CharField(max_length=40, index=True)
    status = fields.CharField(max_length=8, index=True)
    chat_name = fields.TextField()
    config_json = fields.JSONField()
    permission_json = fields.JSONField(default={})
    attach_json = fields.JSONField(default={})

    class Meta:
        table = "peon_chat_config"

class UserWhitelist(Model):

    user_id = fields.CharField(max_length=40, index=True)
    status = fields.CharField(max_length=8)
    created_date = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "peon_user_whitelist"


class ChatWatchUser(Model):
    chat_id = fields.CharField(max_length=40, index=True)
    user_id = fields.CharField(max_length=40, index=True)
    status = fields.CharField(max_length=8)
    attach_json = fields.JSONField()

    class Meta:
        table = "peon_watch_user"

class ChatBehaviorRecord(Model):

    chat_id = fields.CharField(max_length=40, index=True)
    user_id = fields.CharField(max_length=40, index=True)
    full_name = fields.TextField()
    msg_count = fields.IntField()
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "peon_behavior_record"

class ChatDeletedMessage(Model):

    chat_id = fields.CharField(max_length=40, index=True)
    content_type = fields.CharField(max_length=40, index=True)
    message_json = fields.JSONField()
    record_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "peon_deleted_message"