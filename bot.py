from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Application

import os
from dotenv import load_dotenv

from commands.start_timer import start_timer

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    context.user_data['DEFAULT_POMODORO'] = 25
    context.user_data['DEFAULT_BREAK'] = 5

    await update.message.reply_text("Hello! I'm your new bot. How can I assist you?")

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("start_timer", start_timer))
    # application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
