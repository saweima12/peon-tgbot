from sanic import Sanic
from opencc import OpenCC

SERVICE_CODE = "opencc"

def get() -> OpenCC:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

def setup(app: Sanic) -> OpenCC:
    # get configuration from app.config
    converter = OpenCC('s2tw')
    setattr(app.ctx, SERVICE_CODE, converter)
    return converter