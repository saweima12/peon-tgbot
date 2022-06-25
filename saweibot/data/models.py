from saweibot.common.extension import OrjsonBaseModel
from typing import Any, Dict, List, Mapping

from .base import Status


class StatusMapModel(OrjsonBaseModel):
    status_map: Dict[str, Status] = {}

class BotConfigModel(OrjsonBaseModel):
    buffer_size: int = 50
    maintainer: Dict[str, Status] = {}

class ChatConfigModel(OrjsonBaseModel):
    buffer_size: int = 50
    status: Status = Status.OK
    senior_count = 300
    adminstrators: List[str] = []

class ChatWatchUserModel(OrjsonBaseModel):
    user_id: str
    full_name: str = ""
    status: str = "ng"

class ChatMessageModel(OrjsonBaseModel):
    message_id: str
    content_type: str
    is_bot: bool
    user_id: str
    chat_id: str
    content: Any

class ChatBehaviorRecordModel(OrjsonBaseModel):
    full_name: str = ""
    msg_count: int = 0
