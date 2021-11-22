from Neriak import *
from Timer import Timer
import os, GameInput

class Cleric(Persona):
    def __init__(self):
        self.character_name = "Revelation" # Capitalized, set to your character name
        self.server_name = "mischief" # Lowercase, set to your server name
        self.eq_path = os.path.join('F:', 'Games', 'Daybreak Game Company', 'Installed Games', 'EverQuest') # Change this to point to your EQ directory
        self.log_dir = os.path.join(self.eq_path, 'Logs')
        self.key_file = "cleric_keys.ini"
    
        self.log_name = f'eqlog_{self.character_name.lower().capitalize()}_{self.server_name.lower()}.txt'
        self.log_path = os.path.join(self.log_dir, self.log_name)
        self.timers = {} # Name string : Timer object

        super().__init__(__name__, self.log_path, self.key_file)

        # Add any persona specific variables here
        self.casting_cleric_pant = False

        # Add setup here like triggers, actions, etc
        
        # -- 1 -- Auto Cleric Pants
        self.add_trigger(Trigger('pants_toggle', '] (?:Leshy|Leviathan) (?:tells you|tells the group), "toggle cleric pants"'))
        self.add_action(Action('pants_toggle', func=self.toggle_cleric_pants))

        self.add_trigger(Trigger('pants_interrupted', "Your Word of Health spell is interrupted."))
        self.add_action(Action('pants_toggle', self.cast_cleric_pants))

        # -- 2 -- Auto-accept group invitations
        self.add_trigger(Trigger('accept_invites','invites you to join a group.'))
        self.add_action(Action('accept_invites',func=self.accept_invite))
        
        
    
    def load():
        """Returns a new instance of the class"""
        return Cleric()

    def update(self):
        """
        Any long term state can be maintained here. This will get called so that flow of 
        execution can be periodically returned to the player persona. The amount of time between
        calls is a either the time needed to process a particular event or the sleep_time
        parameter passed to Agent.
        """
        try:
            if self.timers['cleric_pants'].alarmed():
                self.cast_cleric_pants()
            
        except KeyError:
            pass

        
    def toggle_cleric_pants(self):
        # If we are already set to auto cast, then toggle off
        if self.cast_cleric_pants:
            self.casting_cleric_pants = False
            GameInput.send('duck')
            try:
                del self.timers['cleric_pants']
            
            except KeyError:
                pass
    
        # Otherwise toggle on
        else:
            self.casting_cleric_pants = True
            self.cast_cleric_pants()
            

    def cast_cleric_pants(self):
        self.timers['cleric_pants'] = Timer()
        self.timers['cleric_pants'].set_alarm(14)
        print("Casting cleric pants!")
        GameInput.send('cleric_pants')
        self.timers['cleric_pants'].start()

    def accept_invites(self):
        


    
        
    