from LogReader import LogReader
import queue, threading, time, re, keyboard, configparser, GameInput, os

class Persona:
    """
    A persona encapsulates the logic of how a character will be played. 
    Two personas might play the same class very differently depending on 
    the desired goal.
    
    The intent is that new player personas will be implemented as sub-classes of Persona,
    which handles implementing the methods needed to setup basic inter-thread communication
    and event handling so that the sub-class can concern itself with the player logic.
    """
    def __init__(self, name):
        self.persona_name = name
        # Read in the configuration file
        self.config = configparser.ConfigParser()
        self.config.read('neriak.ini')
        
        # Log setup
        log_dir = self.config[name]['everquest_log_directory']
        character_name = self.config[name]['character_name'].capitalize()
        server_name = self.config[name]['server_name'].lower()
        log_file_name = f"eqlog_{character_name}_{server_name}.txt"
        full_log_path = os.path.join(log_dir, log_file_name)
        self.log_path = full_log_path
        
        # All of the triggers registered for the Persona.
        # Each trigger has a regex that is evaluated against new entries in the log file
        # and if a match is found the associated action is executed. The triggers and actions
        # are mapped by a common name value.
        self.triggers = []
        self.actions = []
        self.approved_names = self.config[name]['accept_commands_from'].split(',')

    def add_action(self, action):
        """Registers a new action for the persona"""
        self.actions.append(action)

    def add_trigger(self, trigger):
        """Registers a new trigger for the persona"""
        self.triggers.append(trigger)

    def new_custom_action(self, action_name, trigger_string, func, command=False):
        """
        Custom actions that require special logic may pass in a function to be called
        when the event has triggered. If the action is intended to only be triggered by 
        a command from a specific list of people then command should be set to True.
        """
        self.add_trigger(Trigger(action_name, trigger_string))
        self.add_action(Action(action_name, func, command))

    def new_simple_action(self, action_name, trigger_string, command=False):
        """
        Most persona actions are a simple keypress in response to a trigger phrase.
        If the action is intended to only be triggered by a command from a specific 
        list of people then command should be set to True.
        """
        self.add_trigger(Trigger(action_name, trigger_string))
        self.add_action(Action(action_name, self.run_simple_action, command))

    def run_simple_action(self, action_name):
        """
        Executes a simple action.
        """
        print(f"Simple action {action_name} triggered")
        action_key = self.config[self.persona_name][action_name]
        GameInput.send(action_key)
        print(f"Completed simple action {action_name}")

    def get_action_by_name(self, name):
        """Matches a triggered event to a registered action by name."""
        action = None
        for a in self.actions:
            if name == a.name:
                action = a
                break
        
        return action

    def get_config_value(self, key):
        """
        Returns the value for the requested key from the configuration file.
        """
        return self.config[self.persona_name][key]

    def process_event(self, event):
        """Event handler"""
        data = event.match
        action = self.get_action_by_name(event.name)
        
        # Check if this is a command trigger and if so whether
        # it is approved.
        if action.command:
            commander_name = data.group(1)
            print(f"Command issued by {commander_name}... ",end='')
            if not commander_name in self.approved_names:
                print("Denied")
                return
    
            print("Approved")
        action.execute(data)

class Trigger:
    """
    A named regex which when matched triggers an event. 
    This is will be matched against every incoming line from log files.
    """
    def __init__(self, name, regex):
        self.name  = name
        self.regex = re.compile(regex, re.IGNORECASE)

class Event:
    """
    When a Trigger is matched, an event is created which binds 
    the trigger name and the returned regex match object. Ideally
    the regex is designed so that the match groups contain specific
    values of interest for an action to respond to. This can be the
    name of a spell, a character, or the amount of damage taken or 
    healed.
    """
    def __init__(self, name, match):
        """An object to encapsulate a task name and a regular expression match object."""
        self.name  = name
        self.match = match

class Action:
    """An action that an agent may perform such as sending keyboard input or mouseclicks to a window."""
    def __init__(self, name, func, command=False):
        self.name = name
        self.func = func
        self.command = command

    def execute(self, data):
        """Pass in the data from the event to each function in the sequence"""
        print("Executing action")
        self.func(self.name, data)

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
                LogReader(persona, queue).run,
                daemon=True
            )
        
        agent = threading.Thread(target=
                Agent(persona, queue).run,
                daemon=True
            )
        
        # Start execution of producer and consumer threads
        # which will now run independently so long as the
        # main thread is alive.
        reader.start()
        agent.start()
        
        # Block until the hotkey combination is detected at which point the program exits
        keyboard.wait('ctrl+shift+z')

class Agent:
    """Manages the player agent by listening for events and performing actions."""
    def __init__(self, persona, queue, sleep_time=0.1):
        self.queue   = queue
        self.persona = persona
        self.sleep_time = sleep_time

    def run(self):
        """Continuously check queue for new events and manage flow of executionm"""
        print("Agent is running...")
        
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
                event = self.queue.get(block=False)
                #print(f"Got event from queue: {event.name}")
                # Call on the persona to handle the event found
                self.persona.process_event(event)

            except queue.Empty:
                #print("Nothing seen in queue")
                time.sleep(self.sleep_time)
            
            finally:
                self.persona.update()
