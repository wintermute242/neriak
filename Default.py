from Neriak import *
import os

class Default(Persona):
    # CHANGE THESE VALUES
    character_name = "player" # Capitalized, set to your character name
    server_name = "server" # Lowercase, set to your server name
    log_dir = os.path.join('F:', 'Games', 'Daybreak Game Company', 'Installed Games', 'EverQuest', 'Logs') # Change this to your EQ log directory
    
    log_name = f'eqlog_{character_name.lower().capitalize()}_{server_name.lower()}.txt'
    log_path = os.path.join(log_dir, log_name) 

    # Initialize the superclass
    def __init__(self):
        # Add setup here like triggers, actions, etc
        
        
        # This is the last thing that should get called. Don't put anything after this.
        super().__init__(__name__, self.log_path)
    
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

        
    
        
    