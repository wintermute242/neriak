from Neriak import *
import os

class Cleric(Persona):
    # Set character, server, and installation path so that log can be located
    character_name = "revelation" # Capitalized
    server_name = "mischief" # Lowercase
    eq_path = os.path.join('F:', 'Games', 'Daybreak Game Company', 'Installed Games', 'EverQuest') # Change this to point to your EQ directory
    log_dir = os.path.join(eq_path, 'Logs')
    log_name = f'eqlog_{character_name.lower().capitalize()}_{server_name.lower()}.txt'
    log_path = os.path.join(log_dir, log_name) 

    # Initialize the superclass
    def __init__(self):
        super().__init__(__name__, self.log_path)
    
    def load():
        """Returns a new instance of the class"""
        return Cleric()

    def update():
        """
        Any long term state can be maintained here. This will get called so that flow of 
        execution can be periodically returned to the player persona. The amount of time between
        calls is a either the time needed to process a particular event or the sleep_time
        parameter passed to Agent.
        """


    
        
    