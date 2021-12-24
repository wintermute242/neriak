import time, sys, Timer, threading, logging
from Event import Event

class LogReader:
    """
    Designed to run as a producer thread continuously reading the log file and 
    for every specified trigger will send events to a queue shared with the 
    Agent consumer thread to be handled.
    """
    def __init__(self, persona, queue, sleep=0.01):
        self._triggers = persona.triggers
        self._timers = {}

        for trigger in self._triggers:
            if trigger.remote_timer:
                clock = Timer.Timer()
                clock.set_alarm(trigger.remote_timer_max)
                self._timers[trigger.name] = clock
        
        try:
            self._log_file = open(persona.log_file_path, 'r')
            print(f"Opened log file '{persona.log_file_path}'")
        
        except Exception as e:
            print(e)
            sys.exit(1)
        
        self._queue = queue
        self._sleep_time = sleep

    def update_remote_timers(self):
        # This lets you handle events that trigger possibly many times per second
        # so that you are not sending hundreds of messages over the queue that will
        # just end up being ignored anyways.
        for timer_name in self._timers.keys():
            timer = LogReader._timers[timer_name]
            if timer.alarmed():
                LogReader._queue.put(Event(timer_name, 'timer alarmed'))
                timer.reset()


    def generate_next_line(self):
        # A generator to yield the next line in the log file. 
        # If no new lines are found, then sleep.
        while True:
            line = self._log_file.readline()
            if not line:
                self.update_remote_timers()
                # Have to limit this or it will consume 100% CPU
                time.sleep(self._sleep_time)
                continue
            
            # The first 26 characters are just the timestamp
            yield line[27:]
    
    def run(self):
        # Main execution of the thread begins here.
        print(f"Thread[{threading.get_ident()}]: Reading logs...")
        # Initialize the reader to seek to the end of the 
        # current file so that we are reading fresh entries only.
        self._log_file.seek(0,2) 
        
        for line in self.generate_next_line():
            # Every task has a name and a trigger. A trigger is a compiled regex object which is compared against each line from the log file.
            # If a match is found, the label and the associated match object are bundled into an Event object and put
            # into the thread-safe queue. The event will be retrieved and the label evaluated to a matching Task object.
            # This task is then handed the match object (which may contain data it needs) and executed.
            for trigger in self._triggers:
                match = trigger.regex.search(line)
                
                if (match):
                    # Handle any triggers with remote timers
                    if trigger.remote_timer:
                        timer = self._timers[trigger.name]
                        if not timer.is_started():
                            # Send event for only the first trigger of the timer
                            self._queue.put(Event(trigger.name, 'timer started'))
                        timer.start()
                    
                    else:
                        self._queue.put(Event(trigger.name, match, flag=trigger.flag))

        