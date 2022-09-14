from sanic import Sanic

from . import cc
from .cc import get

def register(app: Sanic):
    cc.setup(app)