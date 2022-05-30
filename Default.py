from Neriak import *
import Timer, random

class Default(Persona):
    #--> Initialize any persona specific variables here

    # Initialize the superclass
    def __init__(self):
        super().__init__(__name__, self.log_path, self.key_file)
        #--> Add setup here like triggers, actions, etc
        self.assist_toggle = False
        self.assist_timer = Timer.Timer()
        self.assist_timer.set_alarm(2)
        
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Default()

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
            action_key = self.get_config_value('assist_on')
            if self.assist_timer.alarmed() and self.in_combat:
                GameInput.send(action_key)
                print(f"Performed action 'assist', sent key {action_key}")
                GameInput.pause(0.1)
                self.assist_timer.restart()
                self.assist_timer.set_alarm(random.randint(1,3))
                self.assist_timer.start()

        if self.zoning_follow_timer.alarmed():
            action_key = self.get_config_value('follow_on')
            GameInput.send(action_key)
            print(f"Just zoned. Following.")
            self.zoning_follow_timer.reset()

    def action_toggle_assist(self, action_name, data):
        if action_name == 'assist_on':
            self.assist_timer.set_alarm(random.randint(2,4))
            self.assist_timer.start()
            self.assist_toggle = True
            print(f"Assist toggle ON")

        else:
            self.assist_toggle = False
            print(f"Assist toggle OFF")

    def update_combat_status(self, action_name, data):
        """
        Updates whether we are in combat
        """
        print(f"update_combat_status(): data:{data}")
        if data == 'timer started':
            self.in_combat = True
            print("Now in combat")
        else:
            self.in_combat = False
            print("Exiting combat")

    def follow_after_zoning(self, action_name, data):
        """
        Starts a timer so that we can automatically start following after zoning.
        """
        self.zoning_follow_timer.start()
        print(f"Zoning timer set for {self.zoning_follow_timer.max_time_elapsed} seconds")
        print(f"Started: {self.zoning_follow_timer.timer_started}")
        print(f"Started at: {self.zoning_follow_timer.start_time}")
        
    
        
    