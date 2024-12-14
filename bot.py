from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Application

import os
from dotenv import load_dotenv

from commands.timer import start_timer, pause_timer, stop_timer

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    context.user_data['DEFAULT_POMODORO'] = 25
    context.user_data['DEFAULT_BREAK'] = 5

    await update.message.reply_text("Hello! I'm your pomodoro bot. Let's work together!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("start_timer", start_timer))
    application.add_handler(CommandHandler("pause_timer", pause_timer))
    application.add_handler(CommandHandler("stop_timer", stop_timer))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
