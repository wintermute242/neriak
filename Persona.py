import configparser, sys, GameInput, os
from Event import Event
from Trigger import Trigger

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
        log_dir = self.get_config_value('everquest_log_directory')
        
        try:
            character_name = self.get_config_value('character_name').capitalize()
        except AttributeError:
            print("[Config] Error: No character name provided in neriak.ini")
            sys.exit(1)

        try:
            server_name = self.get_config_value('server_name').lower()
        except AttributeError:
            print("[Config] Error: No server name provided in neriak.ini")
            sys.exit(1)
        
        log_file_name = f"eqlog_{character_name}_{server_name}.txt"
        full_log_path = os.path.join(log_dir, log_file_name)
        self.log_file_path = full_log_path
        
        # All of the triggers registered for the Persona.
        # Each trigger has a regex that is evaluated against new entries in the log file
        # and if a match is found the associated action is executed. The triggers and actions
        # are mapped by a common name value.
        self.triggers = []
        self.actions = []
        self.toggle = {}

        try:
            self.approved_names = [ name.strip() for name in self.get_config_value('accept_commands_from').split(',') ]
        except AttributeError:
            self.approved_names = None

    def get_config_value(self, key):
        """
        Looks up the value of the requested key from the configuration file.
        Returns the value if found, otherwise None.
        """
        value = None
        try:
            value = self.config[self.persona_name][key]
        
        except KeyError:
            pass
        
        return value 

    def process_event(self, event):
        """Event handler"""
        pass