import time

WORK_DURATION = 4  # 25 minutes
SHORT_BREAK_DURATION = 2  # 5 minutes
LONG_BREAK_DURATION = 3  # 15 minutes
POMODOROS_PER_ROUND = 1  # 4 Pomodoros in one round
TOTAL_POMODOROS_ROUND = 1 #

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

class PomodoroTimer:
    def __init__(self):
        self.current_pomodoro = 0  # Number of Pomodoros completed in this round
        self.total_pomodoros = 0  # Total Pomodoros completed across all rounds
        self.current_state = "LONG_BREAK" # "WORK", "SHORT_BREAK", or "LONG_BREAK"
        self.paused = False  # Pause flag
        self.stopped = False  # Stop flag
        self.remaining_time = 0  # Time left when paused


    def next_timer(self):
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


def run_pomodoro():
    timer = PomodoroTimer()

    while not timer.stopped:
        duration = timer.next_timer()
        print(f"Current State: {timer.current_state}")
        print(f"Timer set for: {format_time(duration)}")

        # Countdown Timer
        for remaining in range(duration, 0, -1):
            print(format_time(remaining), end="\r")
            time.sleep(1)  # Wait for 1 second

        print("\nTime's up!")

        if timer.total_pomodoros >= POMODOROS_PER_ROUND * TOTAL_POMODOROS_ROUND:  # Example: stop after 2 rounds
            print("Pomodoro session complete. Great job!")
            break


run_pomodoro()