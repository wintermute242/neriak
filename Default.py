from Neriak import *
import os

class Default(Persona):
    #--> CHANGE THESE VALUES
    character_name = "player" # Capitalized, set to your character name
    server_name = "server" # Lowercase, set to your server name
    eq_path = os.path.join('F:', 'Games', 'Daybreak Game Company', 'Installed Games', 'EverQuest') # Change this to point to your EQ directory
    log_dir = os.path.join(eq_path, 'Logs')
    key_file = "default_keys.ini"
    
    log_name = f'eqlog_{character_name.lower().capitalize()}_{server_name.lower()}.txt'
    log_path = os.path.join(log_dir, log_name)
    
    #--> Initialize any persona specific variables here

    # Initialize the superclass
    def __init__(self):
        super().__init__(__name__, self.log_path, self.key_file)
        #--> Add setup here like triggers, actions, etc
        
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Default()

    def update():
        """
        Any long term state can be maintained here. This will get called so that flow of 
        execution can be periodically returned to the player persona. The amount of time between
        calls is a either the time needed to process a particular event or the sleep_time
        parameter passed to Agent.
        """
        # This gets called roughly every tenth of a second by default. You can do this like
        # check timers to see how much time has elapsed, and take actions if necessary.

        
    
        
    