from saweibot.common.extension import OrjsonBaseModel
from datetime import datetime
from typing import Any, Mapping, List, Union

class AvailableChatSchema(OrjsonBaseModel):
    chat_id: str
    full_name: str
    config_json: Mapping[str, Any] = {}

class ChatMemberPointSchema(OrjsonBaseModel):
    user_id: str
    full_name: str
    point: int
    last_updated: str

class ChatDeleteMessageSchema(OrjsonBaseModel):
    content_type: str
    raw: Union[Mapping[str, Any], List[Any]]
    record_time: str

