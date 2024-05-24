from neriak.util.timer import Timer
import neriak.Neriak as Neriak
import sys
import time

class LogReader:
    """
    Designed to run as a producer thread continuously reading the log file and 
    for every specified trigger will send events to a queue shared with the 
    Agent consumer thread to be handled.
    """
    def __init__(self, persona, queue, sleep=0.01):
        self.triggers = persona.triggers
        self.timers = {}

        for trigger in self.triggers:
            if trigger.remote_timer:
                t = Timer()
                t.set_alarm(trigger.remote_timer_max)
                self.timers[trigger.name] = t
        
        try:
            self.log_file = open(persona.log_file_path, 'r')
            print(f"Opened log file '{persona.log_file_path}'")
        
        except Exception as e:
            print(e)
            sys.exit(1)
        
        self.queue = queue
        self.sleep = sleep

    def update_remote_timers(self):
        for timer_name in self.timers.keys():
            timer = self.timers[timer_name]
            if timer.alarmed():
                self.queue.put(Neriak.Event(timer_name, 'timer alarmed'))
                timer.reset()


    def generate_next_line(self):
        """A generator to yield the next line in the log file. If no new lines are found, then sleep."""
        while True:
            line = self.log_file.readline()
            if not line:
                self.update_remote_timers()
                # Have to limit this or it will consume 100% CPU
                time.sleep(self.sleep)
                continue
            
            # The first 26 characters are just the timestamp
            yield line[27:]
    
    def run(self):
        """Main execution of the thread begins here."""
        print("LogReader running...")
        # Initialize the reader to seek to the end of the 
        # current file so that we are reading fresh entries only.
        self.log_file.seek(0,2) 
        
        for line in self.generate_next_line():
            # Every task has a name and a trigger. A trigger is a compiled regex object which is compared against each line from the log file.
            # If a match is found, the label and the associated match object are bundled into an Event object and put
            # into the thread-safe queue. The event will be retrieved and the label evaluated to a matching Task object.
            # This task is then handed the match object (which may contain data it needs) and executed.
            for trigger in self.triggers:
                #print(f"Checking: [{trigger.regex.pattern}]")
                match = trigger.regex.search(line)
                #print(f"LogReader: {line}",end="")
                if (match):
                    if trigger.remote_timer:
                        timer = self.timers[trigger.name]
                        if not timer.is_started():
                            # Send event for only the first trigger of the timer
                            self.queue.put(Neriak.Event(trigger.name, 'timer started'))
                        timer.start()
                    
                    else:
                        print(f"Matched: {trigger.name}")
                        #print(f"Matched line: [{match.group(0)}]")
                        self.queue.put(Neriak.Event(trigger.name, match))

        