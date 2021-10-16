import time, sys, Neriak

class LogReader:
    """
    Designed to run as a producer thread continuously reading the log file and 
    for every specified trigger will send events to a queue shared with the 
    Agent consumer thread to be handled.
    """
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
        """Stores one or more tasks provided by the persona."""
        for task in tasks:
            self.event_triggers.append(task)

    def generate_next_line(self):
        """A generator to yield the next line in the log file. If no new lines are found, then sleep."""
        while True:
            line = self.log_file.readline()
            if not line:
                time.sleep(self.sleep)
                continue
            
            yield line
    
    def run(self):
        """Main execution of the thread begins here."""
        print("The log reader has started.")
        # Initialize the reader to seek to the end of the 
        # current file so that we are reading fresh entries only.
        self.log_file.seek(0,2) 
        
        for line in self.generate_next_line():
            # Every task has a label and a trigger. A trigger is a compiled regex object which is compared against each line from the log file.
            # If a match is found, the label and the associated match object are bundled into an Event object and put
            # into the thread-safe queue. The event will be retrieved and the label evaluated to a matching Task object.
            # This task is then handed the match object (which may contain data it needs) and executed.
            for task in self.event_triggers:
                m = task.trigger.regex.match(line)
                if (m):
                    self.queue.put(Neriak.Event(task.label, m))

        