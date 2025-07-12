from telegram.ext import Application, CommandHandler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start_command(update, context):
    await update.message.reply_text("✅ Bot is alive! (no MongoDB)")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.run_polling()

if __name__ == "__main__":
    main()
