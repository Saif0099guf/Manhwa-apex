import os
import asyncio
from telegram.ext import Application, CommandHandler
from fastapi import FastAPI
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

app = FastAPI()

@app.get("/")
def home():
    return {"status": "✅ Apex Manhwa Bot is alive!"}

async def start_command(update, context):
    await update.message.reply_text(
        f"👋 Welcome to {BOT_USERNAME}!\nUse /settings to customize your downloads."
    )

async def settings_command(update, context):
    await update.message.reply_text("⚙️ Settings panel will appear here soon.")

async def run_bot():
    print("✅ Starting Apex Bot polling...")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("settings", settings_command))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    uvicorn.run(app, host="0.0.0.0", port=8080)
