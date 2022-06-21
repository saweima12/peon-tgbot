from sanic import Sanic
from sanic.log import logger
from redis.asyncio import Redis

SERVICE_CODE = "redis"

def get() -> Redis:
    app = Sanic.get_app()
    return getattr(app.ctx, SERVICE_CODE)

def setup(app: Sanic) -> Redis:
    # get configuration from app.config
    redis_uri = app.config["REDIS_URI"]
    _redis = Redis.from_url(redis_uri)
    # register redis conenction to ctx
    setattr(app.ctx, SERVICE_CODE, _redis)
    logger.info(f"Register database: {SERVICE_CODE}")
    
    return _redis
    
async def dispose(app: Sanic):
    if hasattr(app.ctx, SERVICE_CODE):
        _redis: Redis = getattr(app.ctx, SERVICE_CODE)
        await _redis.close()
        logger.info(f"Close database: {SERVICE_CODE}")