import asyncio
from fastapi import FastAPI
import uvicorn
from telegram.ext import Application, CommandHandler
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "✅ Apex Manhwa Bot is alive!"}

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

async def start(update, context):
    await update.message.reply_text(
        f"👋 Welcome to {BOT_USERNAME}!\nSend /settings to customize your downloads."
    )

async def settings(update, context):
    await update.message.reply_text("⚙️ Settings panel coming soon...")

async def run_bot():
    app_ = Application.builder().token(BOT_TOKEN).build()
    app_.add_handler(CommandHandler("start", start))
    app_.add_handler(CommandHandler("settings", settings))
    await app_.initialize()
    await app_.start()
    await app_.updater.start_polling()
    await app_.idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    uvicorn.run(app, host="0.0.0.0", port=8080)
