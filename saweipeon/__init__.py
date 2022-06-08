import ujson
from requests import request
from sanic import Sanic, Request, json, text
from telebot import TeleBot
from telebot.types import Message, Update, ChatMember


app = Sanic(__name__)

BOT_TOKEN = ""

bot = TeleBot(BOT_TOKEN)


@app.post('/hook')
async def webhook_handler(request: Request):
    data =  ujson.dumps(request.load_json())
    print(data)
    try:
        _update = Update.de_json(data)
        bot.process_new_updates([_update])
    finally:
        return text("")


@bot.message_handler(commands=["test"])
def test_handle(msg: Message):
    bot.reply_to(msg, ujson.dumps(msg.json))
    

@app.get("/test")
async def get_chat(request: Request):
    admins = bot.get_chat_administrators(-1001165315887)
    for admin in admins:
        print(admin.user.id)
    return text("")
    

@app.before_server_start
async def startup(app: Sanic, loop):
    print("startup")
    bot.set_webhook("https://05bd-211-23-21-139.jp.ngrok.io/hook/")

@app.before_server_stop
async def shutdown(app:Sanic, loop):
    print("shutdown")


@app.get("/")
async def root(request: Request):
    return json({ "yest":"yest"})


# register blueprint


# register bot

