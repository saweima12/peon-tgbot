from saweibot.common.extension import OrjsonBaseModel
from typing import Any, Dict, List

from .base import Status

class StatusMapModel(OrjsonBaseModel):
    status_map: Dict[str, Status] = {}

class ChatConfigModel(OrjsonBaseModel):
    status: Status = Status.OK
    senior_count: int = 300
    check_lowest_count: int = 20
    adminstrators: List[str] = []
    allow_forward:List[str] = []
    block_name_keywords: List[str] = []

class ChatWatchUserModel(OrjsonBaseModel):
    user_id: str
    full_name: str = ""
    status: str = "ng"
    ng_count: int = 0

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

class ChatUrlBlackListModel(OrjsonBaseModel):
    pattern_list: List[str] = []