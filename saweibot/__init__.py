import os
from telebot import TeleBot
from telebot.types import Message, Update, ChatMember

from sanic import Sanic, Request, json, text
from sanic.log import logger
from tortoise.contrib.sanic import register_tortoise

from saweibot import config
from saweibot.db import redis
import saweibot.bots as bots
import saweibot.views as views

# define sanic app
app = Sanic(__name__)
app.update_config(config)

# Loading configure.
env_config_path = os.environ.get("SAWEIBOT_CONFIG")
if env_config_path and os.path.exists(env_config_path):
    app.update_config(env_config_path)

# register database orm.
register_tortoise(app, 
    db_url=app.config['POSTGRES_URI'], 
    modules={"entities": ["saweibot.entities"]}, 
    generate_schemas=True
)

@app.before_server_start
async def startup(app: Sanic, loop):
    await redis.setup(app)

@app.after_server_start
async def configure_service(app: Sanic, loop):
    await bots.register_bots(app)

@app.before_server_stop
async def shutdown(app:Sanic, loop):
    print("shutdown")
    await bots.dispose_bots(app)


# register blueprint
app.blueprint(views.tgbot)
