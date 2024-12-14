import asyncio

class PomodoroTimer:
    def __init__(self, reply_callback=None, update_callback=None):
        self.paused = False
        self.stopped = False
        self.current_phase = "WORK"
        self.current_pomodoro = 0
        self.reply_callback = reply_callback
        self.update_callback = update_callback
        self.last_message_id = None

    async def send_message(self, message, should_save_message_id=False):
        """Send a message using the reply callback."""
        if self.reply_callback:
            last_message_id = await self.reply_callback(message)

            if should_save_message_id:
                self.last_message_id = last_message_id
            else:
                self.last_message_id = None

    async def update_message(self, message):
        if self.update_callback and self.last_message_id:
            await self.update_callback(self.last_message_id, message)

    async def start_timer(self, duration):
        self.stopped = False
        while duration > 0:
            if self.stopped:
                await self.send_message("Timer stopped.")
                return

            if self.paused:
                await asyncio.sleep(1)
                continue


            if self.last_message_id:
                await self.update_message(f"Time remaining in {self.current_phase}: {self.format_time(duration)}")
            else:
                await self.send_message(f"Time remaining in {self.current_phase}: {self.format_time(duration)}", should_save_message_id=True)
            await asyncio.sleep(1)
            duration -= 1

        if duration == 0 and not self.stopped:
            self.last_message_id = None
            await self.send_message(f"{self.current_phase} timer finished!")

    async def run_timer_sequence(self, work_duration, short_break, long_break, rounds):
        for pomodoro in range(1, rounds + 1):
            self.current_phase = "WORK"
            await self.start_timer(work_duration)

            if self.stopped:
                break

            self.current_pomodoro += 1
            if pomodoro < rounds:  # Short break after work
                self.current_phase = "SHORT_BREAK"
                await self.start_timer(short_break)
            elif pomodoro == rounds:  # Long break after the final work interval
                self.current_phase = "LONG_BREAK"
                await self.start_timer(long_break)

        await self.send_message("Pomodoro cycle completed!")

    def pause(self):
        self.paused = not self.paused
        return "paused" if self.paused else "resumed"

    def stop(self):
        self.stopped = True

    @staticmethod
    def format_time(seconds):
        """Format time in MM:SS format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"
