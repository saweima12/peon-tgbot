from sanic import Sanic
from . import test

def register(app: Sanic):
    test.register(app)