from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

import sys
import os

sys.path.append(os.path.abspath("utils"))

from PomodoroTimer import PomodoroTimer

def telegram_reply_callback(update: Update, context: CallbackContext):
    async def reply(message):
        sent_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return sent_message.message_id
    return reply

def telegram_update_callback(update: Update, context: CallbackContext):
    async def reply(message_id, message):
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text=message)
    return reply


async def start_timer(update: Update, context: CallbackContext) -> None:
    pomodoro_time = context.user_data.get('DEFAULT_POMODORO')
    break_time = context.user_data.get('DEFAULT_BREAK')

    reply_callback = telegram_reply_callback(update, context)
    update_callback = telegram_update_callback(update, context)
    timer = PomodoroTimer(reply_callback=reply_callback, update_callback=update_callback)

    while not timer.stopped:
        duration = await timer.next_timer()

        if duration:
            await timer.timer_controller(duration)
