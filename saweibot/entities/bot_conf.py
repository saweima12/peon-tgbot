from tortoise import fields
from tortoise.models import Model

class BotConfig(Model):
    bot_id = fields.CharField(max_length=20, pk=True)
    conf_json = fields.JSONField()
    attach_json = fields.JSONField()

    class Meta:
        table = "bot_config"