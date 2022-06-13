from saweibot.core.extension import OrjsonBaseModel
from typing import Dict, List

from .base import Status

class BotConfigModel(OrjsonBaseModel):
    buffer_size: int = 50

class WhitelistModel(OrjsonBaseModel):
    whitelist_map: Dict[str, Status] = {}

class BlacklistModel(OrjsonBaseModel):
    blacklist_map: Dict[str, Status] = {}

class ChatConfigModel(OrjsonBaseModel):
    buffer_size: int = 50
    status: Status = Status.OK

class FileContentModel(OrjsonBaseModel):
    file_id: str
    status: Status

class FileBlackListModel(OrjsonBaseModel):
    blacklist_map: Dict[str, FileContentModel] = {}
