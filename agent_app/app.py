from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings
)
from botbuilder.schema import Activity
from bot import SimpleAgent
from config import Config

SETTINGS = BotFrameworkAdapterSettings(
    app_id=Config.APP_ID,
    app_password=Config.APP_PASSWORD
)

adapter = BotFrameworkAdapter(SETTINGS)
bot = SimpleAgent()


async def messages(req: web.Request):
    body = await req.json()
    activity = Activity().deserialize(body)

    auth_header = req.headers.get("Authorization", "")

    response = await adapter.process_activity(
        activity, auth_header, bot.on_turn
    )
    if response:
        return web.json_response(data=response.body, status=response.status)
    return web.Response(status=201)


async def health(req):
    return web.Response(text="Bot is running")


app = web.Application()
app.router.add_post("/api/messages", messages)

app.router.add_get("/", health)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
