from telegram import Update
from telegram.ext import ContextTypes

async def start_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pomodoro_time = context.user_data.get('DEFAULT_POMODORO')
    break_time = context.user_data.get('DEFAULT_BREAK')


    await update.message.reply_text(f"We starting {pomodoro_time} {break_time} pomodoros")