from LogReader import LogReader
import queue, threading, time, re, sys

class Persona:
    """
    A persona encapsulates the logic of how a character will be played. 
    Two personas might play the same class very differently depending on 
    the desired goal.
    
    The intent is that new player personas will be implemented as sub-classes of Persona,
    which handles implementing the methods needed to setup basic inter-thread communication
    and event handling so that the sub-class can concern itself with the player logic.
    """
    def __init__(self, name, log_file_path, key_file):
        self.name = name
        self.log_file_path = log_file_path
        self.key_file = key_file
        self.tasks = {}
        self.keys = self.load_keys()

    def load_keys(self) -> dict:
        """
        Loads key/value pairs from a simple ini file. The key is an arbitrary name to give to
        a particular keypress so as to better document what is being accomplished by an action.
        """
        keys = {}
        try:
            with open(self.key_file) as key_file:
                for line in key_file:
                    if '=' in line:
                        key, value = line.split('=')
                        key = key.strip().lower()
                        value = value.strip().lower()
                        keys[key] = value

        except Exception as e:
            print(e)


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

class Trigger:
    """
    A named regex which when matched triggers an event. 
    This is will be matched against every incoming line from log files.
    """
    def __init__(self, name, regex):
        self.name  = name
        self.regex = re.compile(regex)

class Event:
    """
    When a Trigger is matched, an event is created which binds 
    the trigger name and the returned regex match object. Ideally
    the regex is designed so that the match groups contain specific
    values of interest for an action to respond to. This can be the
    name of a spell, a character, or the amount of damage taken or 
    healed.
    """
    def __init__(self, task_label, match):
        """An object to encapsulate a task label and a regular expression match."""
        self.label  = task_label
        self.match  = match

class Action:
    """An action that an agent may perform such as sending keyboard input or mouseclicks to a window."""
    def __init__(self, func=None):
        self.sequence = []
        # Syntactic sugar for cases when there will only be one sequence function
        if func:
            self.add_sequence_item(func)


    def add_sequence_item(self, func):
        """Take a function and appends it to a list of items to be executed."""
        self.sequence.append(func)

    def execute(self, data):
        """Pass in the data from the event to each function in the sequence"""
        for item in self.sequence:
            item(data)

class Task:
    """A task is a trigger and a set of one or more actions which has a label that identifies it."""
    def __init__(self, label, trigger, action=None):
        self.label   = label
        self.actions = []
        self.trigger = trigger
        # Syntactic sugar for cases when there will only be one action
        if action:
            self.add_action(action)

    def add_action(self, action):
        self.actions.append(action)

    def execute(self, data):
        for action in self.actions:
            action.execute(data)

class Controller():
    """
    Responsible for setting up the shared objects used for inter-thread
    communication and then creating the independent producer and consumer worker threads. 
    This is the 'main' thread which responds to user input like keyboard interrupts to 
    stop all execution.
    """
    def __init__(self, persona):
        self.queue  = queue.Queue()
        self.persona = persona
    
    def run(self):
        persona = self.persona
        queue = self.queue

        # Set daemon flag so that new threads stop
        # once the main thread calls system.exit().
        reader = threading.Thread(target=
                LogReader(persona, self.queue).run,
                daemon=True
            )
        
        agent = threading.Thread(target=
                Agent(persona, self.queue).run,
                daemon=True
            )
        
        # Start execution of producer and consumer threads
        # which will now run independently so long as the
        # main thread is alive.
        reader.start()
        agent.start()
        
        # Control is returned to main thread. Periodically
        # check whether the user wants to end the program.
        # When detected, this will abrubtly terminate all 
        # daemon threads as well.
        try:
            while True:
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            sys.exit(0)

class Agent:
    """Manages the player agent by listening for events and performing actions."""
    def __init__(self, persona, queue, sleep_time=0.1):
        self.queue   = queue
        self.persona = persona
        self.sleep_time = sleep_time

    def run(self):
        """Continuously check queue for new events and manage flow of executionm"""
        print("The agent has started.")
        
        # Looking for the main event loop handling triggered events? This is it.
        # The agent will continuosly check for triggered events and send them
        # to the persona to be handled in a first-in-first-out order.
        #
        # Either an event will be handled or, if there are no events, the agent
        # will temporarily go to sleep. After either of these cases complete the agent
        # will then be given an opportunity to update its state and do whatever other
        # work it needs to do.
        #
        # This is important as it allows the agent to build and maintain a more
        # complex internal state and respond to circumstances over a longer time horizon 
        # than reacting immediately to a single event. Things like measuring damage
        # taken over a certain interval, or doing a thing every n seconds might
        # be implemented in update(). It is a way to periodically return control of 
        # execution back to the persona to do whatever it needs to do.
        while True:
            try:
                event = self.queue.get()
                print(f"Got event from queue: {event.label}")
                # Call on the persona to handle the event found
                self.persona.process_event(event)

            except queue.Empty:
                print("Nothing seen in queue")
                time.sleep(self.sleep_time)
            
            finally:
                self.persona.update()

    def stop(self):
        sys.exit()
