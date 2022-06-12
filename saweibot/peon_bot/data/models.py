from saweibot.core.extension import OrjsonBaseModel
from typing import Dict

class BotConfigModel(OrjsonBaseModel):
    buffer_size: int = 50


class ChatWhitelistModel(OrjsonBaseModel):
    whitelist_map: Dict[str, str] = {}
