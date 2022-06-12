import orjson
from pydantic import BaseModel

def orjson_dumps(v, *, default) -> str:
    # orjson.dumps returns bytes, need to decode.
    return orjson.dumps(v, default=default).decode()

class OrjsonBaseModel(BaseModel):
    
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
