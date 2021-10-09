from Event import Event
import time

class LogReader:
    """Handles continuously reading the log file and sends events to a queue based on triggers."""
    def __init__(self, persona, queue, sleep=0.1):
        self.event_triggers = []
        self.persona        = persona
        self.log_file_path  = persona.log_file_path
        self.log_file       = None
        
        try:
            self.log_file = open(self.log_file_path, 'r')
            print(f"Opened log file '{self.log_file_path}'")
        except Exception as e:
            print(e)
        
        self.queue = queue
        self.sleep = sleep

        self.register_event(persona.get_tasks())


    def register_event(self, tasks):
        """Stores one or more event tasks of class Task."""
        for task in tasks:
            self.event_triggers.append(task)

    def generate_next_line(self):
        """A generator to yield the next line in the log file. If no new lines or found then sleep."""
        while True:
            line = self.log_file.readline()
            if not line:
                time.sleep(self.sleep)
                continue
            yield line
    
    def run(self):
        """Begin reading the log file and comparing lines to the current list of triggers."""
        print("The log reader has started.")
        self.log_file.seek(0,2) # Seek to the end of the current file
        
        for line in self.generate_next_line():
            # Every task has a label and a trigger. A trigger is a compiled regex object which is compared against each line from the log file.
            # If a match is found, the label and the associated match object are bundled into an Event object and put
            # into the thread-safe queue. The event will be retrieved and the label evaluated to a matching Task object.
            # This task is then handed the match object (which may contain data it needs) and executed.
            for task in self.event_triggers:
                m = task.trigger.regex.match(line)
                if (m):
                    self.queue.put(Event(task.label, m))

        