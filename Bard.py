from Neriak import *
import os, GameInput, Timer, random

class Bard(Persona):
    #--> CHANGE THESE VALUES
    character_name = "Gillea" # Capitalized, set to your character name
    server_name = "mischief" # Lowercase, set to your server name
    eq_path = os.path.join('F:', 'Games', 'Daybreak Game Company', 'Installed Games', 'EverQuest') # Change this to point to your EQ directory
    log_dir = os.path.join(eq_path, 'Logs')
    key_file = "bard_keys.ini"
    
    
    log_name = f'eqlog_{character_name.lower().capitalize()}_{server_name.lower()}.txt'
    log_path = os.path.join(log_dir, log_name)
    
    #--> Initialize any persona specific variables here

    # Initialize the superclass
    def __init__(self):
        super().__init__(name=__name__, log=self.log_path, keys=self.key_file)
        self.assist_toggle = False
        self.assist_timer = Timer.Timer()
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
        self.add_trigger(Trigger('follow', """(\w+) tells the group, 'follow me'"""))
        self.add_action(Action('follow', self.action_follow))
        self.add_trigger(Trigger('stop_follow', """(\w+) tells the group, 'stop following'"""))
        self.add_action(Action('stop_follow', self.action_stop_follow))

        # Starting/stopping melody
        self.add_trigger(Trigger('toggle_songs', """(\w+) tells the group, 'songs'"""))
        self.add_action(Action('toggle_songs', self.action_toggle_songs))

        # Swapping bandolier
        self.add_trigger(Trigger('bandolier', """(\w+) tells the group, 'gillea swap to (\w+)'"""))
        self.add_action(Action('bandolier', self.action_bandolier))

        # Assist
        self.add_trigger(Trigger('assist_on', """(\w+) tells the group, '(assist me)'"""))
        self.add_action(Action('assist_on', self.action_toggle_assist))
        self.add_trigger(Trigger('assist_off', """(\w+) tells the group, '(stop assisting)'"""))
        self.add_action(Action('assist_off', self.action_toggle_assist))
        
        
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Bard()

    def add_approved_name(self, name):
        self.approved_names.append(name.strip().lower())

    def is_name_approved(self, name) -> bool:
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
        if self.assist_toggle:
            action_key = self.keys['assist']
            if (self.assist_timer.alarmed()):
                GameInput.send(action_key)
                print(f"Performed action 'assist', sent key {action_key}")
                self.assist_timer.restart()
                self.assist_timer.set_alarm(random.randint(1,3))
                self.assist_timer.start()

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
    
    def action_toggle_songs(self, data):
        print(f"Data: [{data.group(0)}]")
        player_name = data.group(1)
        print(f"Received request to toggle songs from {player_name}")
        action_key = self.keys['toggle_songs']
        if self.is_name_approved(player_name):
            GameInput.send(action_key)
            print(f"Performed action 'toggle_songs', sent key {action_key}")

    def action_bandolier(self, data):
        print(f"Data: [{data.group(0)}]")
        player_name = data.group(1)
        bandolier_name = data.group(2)
        print(f"Received request to swap to bandolier {bandolier_name} from {player_name}")
        action_key = self.keys[bandolier_name]
        if self.is_name_approved(player_name):
            GameInput.send(action_key)
            print(f"Performed action 'bandolier:{bandolier_name}', sent key {action_key}")

    def action_toggle_assist(self, data):
        switch_on = False
        print(f"Data: [{data.group(0)}]")
        player_name = data.group(1)
        assist_command = data.group(2)
        if assist_command == 'assist me':
            switch_on = True
        
        print(f"Received request to assist:{switch_on} from {player_name}")
        if switch_on:
            self.assist_timer.set_alarm(random.randint(1,3))
            self.assist_timer.start()

            if self.is_name_approved(player_name):
                self.assist_toggle = True

        else:
            self.assist_toggle = False

    