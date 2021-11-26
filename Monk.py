from Neriak import *
import os, GameInput, Timer, random

class Monk(Persona):
    #--> CHANGE THESE VALUES
    character_name = "Nakai" # Capitalized, set to your character name
    server_name = "mischief" # Lowercase, set to your server name
    eq_path = os.path.join('C:\\', 'Users', 'Public', 'Daybreak Game Company', 'Installed Games', 'EverQuest') # Change this to point to your EQ directory
    log_dir = os.path.join(eq_path, 'Logs')
    key_file = "monk_keys.ini"
    
    
    log_name = f'eqlog_{character_name.lower().capitalize()}_{server_name.lower()}.txt'
    log_path = os.path.join(log_dir, log_name)
    
    #--> Initialize any persona specific variables here

    # Initialize the superclass
    def __init__(self):
        super().__init__(name=__name__, log=self.log_path, keys=self.key_file)
        self.assist_toggle = False
        self.assist_timer = Timer.Timer()
        self.assist_timer.set_alarm(2)
        self.avatar_timer = Timer.Timer()
        self.avatar_timer.set_alarm(230)
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
        self.add_trigger(Trigger('follow', """(\w+) tells (?:you|the group), 'follow me"""))
        self.add_action(Action('follow', self.action_follow))
        self.add_trigger(Trigger('stop_follow', """(\w+) tells (?:you|the group), 'stop following"""))
        self.add_action(Action('stop_follow', self.action_stop_follow))

        # Avatar proc
        self.add_trigger(Trigger('avatar', """Your body screams with the power of an Avatar"""))
        self.add_action(Action('avatar', self.action_avatar))

        # Assist
        self.add_trigger(Trigger('assist_on', """(\w+) tells (?:you|the group), '(assist me)"""))
        self.add_action(Action('assist_on', self.action_toggle_assist))
        self.add_trigger(Trigger('assist_off', """(\w+) tells (?:you|the group), '(stop assisting)"""))
        self.add_action(Action('assist_off', self.action_toggle_assist))

        # DPS burn
        self.add_trigger(Trigger('burn', """(\w+) tells (?:you|the group), '(burn)"""))
        self.add_action(Action('burn', self.action_burn))
        
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Monk()

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
            evade_key = self.keys['evade']
            if self.assist_timer.alarmed():
                GameInput.send(action_key)
                print(f"Performed action 'assist', sent key {action_key}")
                GameInput.pause(0.1)
                GameInput.send(evade_key)
                self.assist_timer.restart()
                self.assist_timer.set_alarm(random.randint(1,3))
                self.assist_timer.start()

        if self.avatar_timer.alarmed():
            action_key = self.keys['swap_to_avatar']
            GameInput.send(action_key)
            print(f"Performed action 'swap_to_avatar_weapons', sent key {action_key}")
            self.avatar_timer.reset()


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

    def action_avatar(self, data):
        print(f"Avatar procced")
        action_key = self.keys['swap_to_main']
        GameInput.send(action_key)
        print(f"Performed action 'swap_to_main', sent key {action_key}")
        self.avatar_timer.set_alarm(230)
        self.avatar_timer.start()

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

        def action_burn(self, data):
            action_key = self.keys['burn']
            GameInput.send(action_key)
            print(f"Performed action 'burn', sent key {action_key}")