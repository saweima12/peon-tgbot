from datetime import datetime as dt
from urllib import request
from sanic import Sanic, Request
from sanic.log import logger
from sanic.response import HTTPResponse

def register(app: Sanic):

    async def attach_time(request: Request):
        request.ctx.start_time = dt.utcnow()

    async def print_time(request: Request, response: HTTPResponse):
        if hasattr(request.ctx, "start_time"):
            logger.debug(f"Spend time: {dt.utcnow() - request.ctx.start_time}")

    @app.main_process_start
    async def on_startup(app: Sanic):
        app.register_middleware(attach_time, "request")
        app.register_middleware(print_time, "response")
        logger.debug("DeubgMode: Attach test middleware.")