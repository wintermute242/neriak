from pydirectinput import FailSafeException
from Neriak import *
import os, GameInput, Timer, random

class Cleric(Persona):
    #--> CHANGE THESE VALUES
    character_name = "Revelation" # Capitalized, set to your character name
    server_name = "mischief" # Lowercase, set to your server name
    eq_path = os.path.join('C:\\', 'Users', 'Public', 'Daybreak Game Company', 'Installed Games', 'EverQuest') # Change this to point to your EQ directory
    log_dir = os.path.join(eq_path, 'Logs')
    key_file = "cleric_keys.ini"
    
    
    log_name = f'eqlog_{character_name.lower().capitalize()}_{server_name.lower()}.txt'
    log_path = os.path.join(log_dir, log_name)
    
    #--> Initialize any persona specific variables here

    # Initialize the superclass
    def __init__(self):
        super().__init__(name=__name__, log=self.log_path, keys=self.key_file)
        self.pants_toggle = False
        self.pants_timer = Timer.Timer()
        self.pants_timer.max_time_elapsed = 12
        self.approved_names = []
        self.keys = {}

        # Load the keys from the ini file.
        # The key is a name matched in this program for
        # the intended action and the value is the corresponding 
        # key stroke(s) sent to the game to accomplish this.
        with open(self.key_file, 'r') as file:
            for line in file:
                key, value = line.strip().lower().split('=')
                self.keys[key] = value.strip('\n')
        
        #--> Add setup here like triggers, actions, etc

        for name in ['Leviathan','Leshy','Orkamungus','Blighted']:
            self.add_approved_name(name)

        # Following
        self.add_trigger(Trigger('follow', """(\w+) tells the group, 'follow me"""))
        self.add_action(Action('follow', self.action_follow))
        self.add_trigger(Trigger('stop_follow', """(\w+) tells the group, 'stop following"""))
        self.add_action(Action('stop_follow', self.action_stop_follow))

        # Starting/stopping melody
        self.add_trigger(Trigger('toggle_pants', """(\w+) tells the group, 'cast those pants"""))
        self.add_action(Action('toggle_pants', self.action_toggle_pants))
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Cleric()

    def add_approved_name(self, name):
        self.approved_names.append(name.strip().lower())

    def is_name_approved(self, name) -> bool:
        # Returns true or false depending on whether the person stating the name
        # is allowed to send requests.
        name = name.strip().lower()
        result = False
        if name in self.approved_names:
            result = True
        return result

    def update(self):
        """
        Any long term state can be maintained here. This will get called so that flow of 
        execution can be periodically returned to the player persona. The amount of time between
        calls is a either the time needed to process a particular event or the sleep_time
        parameter passed to Agent.
        """
        # This gets called roughly every tenth of a second by default. You can do this like
        # check timers to see how much time has elapsed, and take actions if necessary.
        if self.pants_toggle:
            action_key = self.keys['cast_pants']
            if (self.pants_timer.alarmed()):
                GameInput.send(action_key)
                print(f"Performed action 'cast pants', sent key {action_key}")
                self.pants_timer.restart()
                self.pants_timer.start()

    def action_follow(self, data):
        print(f"Data: [{data.group(0)}]")
        player_name = data.group(1)
        print(f"Received request to follow from {player_name}")
        action_key = self.keys['follow']
        if self.is_name_approved(player_name):
            GameInput.send(action_key)
            print(f"Performed action 'follow', sent key {action_key}")

    def action_stop_follow(self, data):
        print(f"Data: [{data.group(0)}]")
        player_name = data.group(1)
        print(f"Received request to stop follow from {player_name}")
        action_key = self.keys['stop_follow']
        if self.is_name_approved(player_name):
            GameInput.send(action_key)
            print(f"Performed action 'stop_follow', sent key {action_key}")
    
    def action_toggle_pants(self, data):
        print(f"Data: [{data.group(0)}]")
        player_name = data.group(1)
        print(f"Received request to toggle pants from {player_name}")
        if self.is_name_approved(player_name):
            if self.action_toggle_pants:
                self.action_toggle_pants = False
            else:
                action_key = self.keys['cast_pants']
                GameInput.send(action_key)
                print(f"Performed action 'toggle_pants', sent key {action_key}")
                self.pants_toggle = True
                self.pants_timer.start()