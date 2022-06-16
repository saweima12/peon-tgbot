from sanic import Sanic
from types import ModuleType
from typing import Dict, Iterable

from . import peon_bot

def register(app: Sanic, orm_modules: dict):
    peon_bot.register_bot(app, orm_modules)