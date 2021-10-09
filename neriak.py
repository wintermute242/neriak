from LogReader import LogReader
import queue, threading, time, re, sys

class Controller():
    """Coordinates setup of worker threads and shared memory objects."""
    def __init__(self, persona):
        self.queue  = queue.Queue()
        self.persona = persona
    
    def run(self):
        persona = self.persona
        queue = self.queue

        reader = threading.Thread(target=
                LogReader(persona, self.queue).run,
                daemon=True
            )
        
        agent = threading.Thread(target=
                Agent(persona, self.queue).run,
                daemon=True
            )
        
        reader.start()
        agent.start()
        
        # Go into an infinite loop and wait for the program to be terminated.
        try:
            while True:
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            reader.stop()
            agent.stop()

class Persona:
    """A persona encapsulates the logic behind how a character will be played. Two personas might play the same class very differently depending on the desired goal."""
    def __init__(self, name, log_file_path):
        self.name = name
        self.log_file_path = log_file_path
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.label] = task

    def get_tasks(self):
        return self.tasks.values()

    def get_task_by_label(self, name):
        return self.tasks[name]

    def process_event(self, event):
        data = event.match
        task = self.get_task_by_label(event.label)
        task.execute(data)

class Agent:
    def __init__(self, persona, queue):
        self.queue   = queue
        self.persona = persona

    def run(self):
        """Continuously check queue for new events"""
        print("The agent has started.")
        while True:
            try:
                event = self.queue.get()
                print(f"Got event from queue: {event.label}")
                self.persona.process_event(event)
            except queue.Empty:
                print("Nothing seen in queue")
                time.sleep(0.1)

    def stop(self):
        sys.exit()

class Task:
    def __init__(self, label, trigger, actions):
        self.label   = label
        self.actions = []
        self.trigger = trigger
        for action in actions:
            self.actions.append(action)

    def execute(self, data):
        for action in self.actions:
            action.execute(data)

class Trigger:
    """An object encapsulating a regex and a trigger name."""
    def __init__(self, name, regex):
        self.name  = name
        self.regex = re.compile(regex)

class Action:
    def __init__(self, name):
        self.name = name
        self.sequence = []

    def add_sequence_item(self, func):
        """Take a function and appends it to a list of items to be executed."""
        self.sequence.append(func)

    def execute(self, data):
        for item in self.sequence:
            item(data)

class Event:
    def __init__(self, task_label, match):
        """An object to encapsulate a task label and a regular expression match."""
        self.label  = task_label
        self.match  = match
