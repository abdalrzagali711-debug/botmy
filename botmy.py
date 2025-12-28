import os
import asyncio
from telegram.ext import Application, CommandHandler
from aiohttp import web

TOKEN = os.getenv("TOKEN")

async def start(update, context):
    await update.message.reply_text("البوت شغال 😎")

async def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    bot_task = asyncio.create_task(run_bot())
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    await bot_task

asyncio.run(main())
