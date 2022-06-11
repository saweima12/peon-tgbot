from tortoise import fields
from tortoise.models import Model

class PeonBehaviorRecord(Model):
    chat_id = fields.BigIntField(index=True)
    user_id = fields.BigIntField(index=True)
    counter = fields.IntField()

    class Meta:
        table = "peon_behavior_record"

class PeonContentBlacklist(Model):
    
    chat_id = fields.BigIntField(index=True)
    content_type = fields.CharField(max_length=100)
    file_id = fields.TextField()
    file_unique_id = fields.TextField()
    status = fields.CharField(max_length=8)

    class Meta:
        table = "peon_content_blacklist"

class PeonChatConfig(Model):
    
    chat_id = fields.BigIntField(index=True)
    config_json = fields.JSONField()
    permission_json = fields.JSONField()
    attach_json = fields.JSONField()

    class Meta:
        table = "peon_chat_config"

class PeonChatWhitelist(Model):
    bot_id = fields.CharField(max_length=20, index=True)
    chat_id = fields.BigIntField(index=True)
    status = fields.CharField(max_length=8)
    created_date = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "peon_chat_whitelist"