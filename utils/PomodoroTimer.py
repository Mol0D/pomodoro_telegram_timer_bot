import time
from Message import *

WORK_DURATION = 25  # 25 minutes
SHORT_BREAK_DURATION = 5  # 5 minutes
LONG_BREAK_DURATION = 10  # 15 minutes
POMODOROS_PER_ROUND = 2  # 4 Pomodoros in one round
TOTAL_POMODOROS_ROUND = 2 #

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

class PomodoroTimer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # Use super().__new__() for cleaner code in Python 3
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, reply_callback, update_callback):
        self.current_pomodoro = 0  # Number of Pomodoros completed in this round
        self.total_pomodoros = 0  # Total Pomodoros completed across all rounds
        self.current_state = "LONG_BREAK" # "WORK", "SHORT_BREAK", or "LONG_BREAK"
        self.paused = False  # Pause flag
        self.stopped = False  # Stop flag
        self.remaining_time = 0  # Time left when paused
        self.reply_callback = reply_callback  # Callback to send a new message
        self.update_callback = update_callback  # Callback to update the last message
        self.last_message_id = None  # ID of the last sent message

    async def send_message(self, message):
        if self.reply_callback:
            self.last_message_id = await self.reply_callback(message)

    async def update_message(self, message):
        if self.update_callback and self.last_message_id:
            await self.update_callback(self.last_message_id, message)

    async def timer_controller(self, duration):
        self.remaining_time = duration
        await self.send_message(f"Timer started for {format_time(duration)} in {self.current_state} mode.")

        while self.remaining_time > 0 and not self.stopped:
            if self.paused:
                time.sleep(1)  # Check every second if the pause is lifted
                continue

            # Countdown
            await self.update_message(f"Time remaining: {format_time(self.remaining_time)}")
            time.sleep(1)
            self.remaining_time -= 1

        if self.stopped:
            await self.update_message("\nTimer stopped.")
        elif self.remaining_time == 0:
            await self.update_message("\nTime's up!")

    async def next_timer(self):
        if self.total_pomodoros >= POMODOROS_PER_ROUND * TOTAL_POMODOROS_ROUND:  # Example: stop after 2 rounds
            await self.send_message("Pomodoro session complete. Great job!")
            self.stopped = True
            return

        # Logic to switch states
        if self.current_state == "WORK":
            if self.current_pomodoro % POMODOROS_PER_ROUND == 0:
                self.current_state = "LONG_BREAK"
                return LONG_BREAK_DURATION
            else:
                self.current_state = "SHORT_BREAK"
                return SHORT_BREAK_DURATION
        elif self.current_state in ("SHORT_BREAK", "LONG_BREAK"):
            self.current_state = "WORK"
            self.current_pomodoro += 1
            self.total_pomodoros += 1
            return WORK_DURATION

    async def pause(self):
        self.paused = not self.paused
        state = "paused" if self.paused else "resumed"
        await self.send_message(f"Timer {state}.")

    async def stop(self):
        self.stopped = True
        await self.send_message("Stopping timer...")
