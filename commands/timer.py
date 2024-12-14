from telegram import Update
from telegram.ext import CallbackContext
import asyncio

import sys
import os

sys.path.append(os.path.abspath("utils"))

from PomodoroTimer import PomodoroTimer

# Specify durations in minutes
WORK_DURATION_MINUTES = 25  # Standard Pomodoro work session
SHORT_BREAK_MINUTES = 5     # Short break duration
LONG_BREAK_MINUTES = 15     # Long break duration
POMODOROS_PER_ROUND = 2  # 4 Pomodoros in one round

# Convert to seconds for use in the timer
WORK_DURATION = WORK_DURATION_MINUTES * 60
SHORT_BREAK = SHORT_BREAK_MINUTES * 60
LONG_BREAK = LONG_BREAK_MINUTES * 60

async def start_timer(update: Update, context: CallbackContext):
    if "timer" not in context.user_data:
        async def reply_callback(message):
            sent_message = await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            return sent_message.message_id

        async def update_message_callback(message_id, message):
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id,
                                                    text=message)

        context.user_data["timer"] = PomodoroTimer(reply_callback=reply_callback, update_callback=update_message_callback)

    timer = context.user_data["timer"]

    if "task" in context.user_data and not context.user_data["task"].done():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Timer is already running!")
        return

    context.user_data["task"] = asyncio.create_task(
        timer.run_timer_sequence(WORK_DURATION, SHORT_BREAK, LONG_BREAK, POMODOROS_PER_ROUND)
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Pomodoro timer started!")

async def pause_timer(update: Update, context: CallbackContext):
    if "timer" in context.user_data:
        timer = context.user_data["timer"]
        state = timer.pause()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Timer {state}.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No active timer to pause!")

async def stop_timer(update: Update, context: CallbackContext):
    if "timer" in context.user_data:
        timer = context.user_data["timer"]
        timer.stop()

        # Cancel the running task
        if "task" in context.user_data and not context.user_data["task"].done():
            context.user_data["task"].cancel()
            try:
                await context.user_data["task"]
            except asyncio.CancelledError:
                pass

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Timer stopped.")
        del context.user_data["timer"]
        del context.user_data["task"]
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No active timer to stop!")
