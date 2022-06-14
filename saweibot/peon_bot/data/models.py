from saweibot.core.extension import OrjsonBaseModel
from typing import Any, Dict, List

from .base import Status

class WhitelistModel(OrjsonBaseModel):
    whitelist_map: Dict[str, Status] = {}

class BlacklistModel(OrjsonBaseModel):
    blacklist_map: Dict[str, Status] = {}

class BotConfigModel(OrjsonBaseModel):
    buffer_size: int = 50
    maintainer: Dict[str, Status] = {}

class ChatConfigModel(OrjsonBaseModel):
    buffer_size: int = 50
    status: Status = Status.OK

class ChatMessageModel(OrjsonBaseModel):
    message_id: str
    content_type: str
    is_bot: bool
    user_id: str
    chat_id: str
    content: Any

class FileContentModel(OrjsonBaseModel):
    file_id: str
    status: Status = Status.OK

class FileBlackListModel(OrjsonBaseModel):
    blacklist_map: Dict[str, FileContentModel] = {}
