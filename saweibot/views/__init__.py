
from sanic import Sanic

from . import dataview, bot


def register_route(app: Sanic):
    # register blueprint.
    app.blueprint(dataview.bp)
    app.blueprint(bot.bp)