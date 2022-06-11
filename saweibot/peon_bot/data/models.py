from lib2to3.pytree import Base
from pydantic import BaseModel

class PeonBotConfig(BaseModel):
    buffer_size: int = 50


class PeonBotWhitelist(BaseModel):
    pass
