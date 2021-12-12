import time

class Timer:
    """Simple timer class to emulate a stop watch with alarm settings."""
    def __init__(self):
        self.start_time = None
        self.max_time_elapsed = 0
        self.time_elapsed = 0
        self.timer_started = False

    def set_alarm(self, seconds):
        """Set the alarm to go off after the specified number of seconds"""
        self.max_time_elapsed = seconds

    def start(self):
        """Start the timer by storing the current time."""
        self.start_time = time.time()
        self.timer_started = True

    def stop(self):
        """Stop the timer and store the number of elapsed seconds."""
        now = time.time()
        self.time_elapsed = now - self.start_time

    def alarmed(self) -> bool:
        """Check whether the timer has alarmed."""
        now = time.time()

        try:
            self.time_elapsed = now - self.start_time
            if self.time_elapsed > self.max_time_elapsed:
                return True
        
        except TypeError:
            pass
        
        return False

    def is_started(self):
        return self.timer_started

    def reset(self):
        """Resets the cumulative time"""
        self.time_elapsed = 0
        self.start_time = None

    def restart(self):
        """Restart the timer."""
        self.stop()
        self.reset()
        self.start()