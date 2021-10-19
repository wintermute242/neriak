from Neriak import *
from Timer import Timer
import os, GameInput

class Warrior(Persona):
    # Initialize the superclass
    def __init__(self):
        self.character_name = "Leviathan" # Capitalized, set to your character name
        self.server_name = "mischief" # Lowercase, set to your server name
        self.eq_path = os.path.join('F:', 'Games', 'Daybreak Game Company', 'Installed Games', 'EverQuest') # Change this to point to your EQ directory
        self.log_dir = os.path.join(self.eq_path, 'Logs')
        self.key_file = "warrior_keys.ini"
    
        self.log_name = f'eqlog_{self.character_name.lower().capitalize()}_{self.server_name.lower()}.txt'
        self.log_path = os.path.join(self.log_dir, self.log_name)
        self.timers = {} # Name string : Timer object

        # Add any persona specific variables here
        
        # Add setup here like triggers, actions, etc
        
        # -- 1 -- Auto Avatar
        avatar_trigger = Trigger("avatar_proc", "^Your body screams with the power of an avatar")
        avatar_action  = Action(func=self.avatar_proc)
        avatar_task    = Task('avatar_proc',avatar_trigger, action=avatar_action)
        self.add_task(avatar_task)

        
        # This is the last thing that should get called. Don't put anything after this.
        super().__init__(__name__, self.log_path, self.key_file)
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Warrior()

    def update(self):
        """
        Any long term state can be maintained here. This will get called so that flow of 
        execution can be periodically returned to the player persona. The amount of time between
        calls is a either the time needed to process a particular event or the sleep_time
        parameter passed to Agent.
        """
        # This gets called roughly every tenth of a second by default. You can do this like
        # check timers to see how much time has elapsed, and take actions if necessary. 

        # Check if we need to swap to avatar
        if self.timers['avatar'].alarmed():
            # Swap to avatar weapons
            GameInput.send(self.keys['avatar'])

    def avatar_proc(self, data):
        """Called whenever avatar procs"""
        try:
            self.timers['avatar'].restart()
            
        except KeyError:
            timer = Timer()
            alarm_seconds = 240 # 4 minutes
            timer.set_alarm(alarm_seconds)
            timer.start()
            self.timers['avatar'] = timer





        
    
        
    