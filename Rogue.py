from Neriak import *
from Default import Default
import GameInput, Timer, random

class Rogue(Default):
    # Initialize the superclass
    def __init__(self):
        super().__init__(name=__name__)
        #--> Add setup here like triggers, actions, etc

        # Avatar proc
        self.new_custom_action('avatar', """Your body screams with the power of an Avatar""", self.action_avatar)
        self.avatar_timer = Timer.Timer()
        self.avatar_timer.set_alarm(230)

        # Assist
        self.new_custom_action('assist_on', """(\w+) tells (?:you|the group), '(assist me)""", 
            self.action_toggle_assist, command=True)
        self.new_custom_action('assist_off', """(\w+) tells (?:you|the group), '(stop assisting)""", 
            self.action_toggle_assist, command=True)
        self.assist_toggle = False
        self.assist_timer = Timer.Timer()
        self.assist_timer.set_alarm(2)

        # DPS burn
        self.new_simple_action('disc_burn', """(\w+) tells (?:you|the group), '(burn)""", command=True)
        

    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Rogue()

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
            evade_key = self.get_config_value('evade')

            if self.assist_timer.alarmed() and self.in_combat:
                GameInput.send(action_key)
                print(f"Performed action 'assist', sent key {action_key}")
                GameInput.pause(0.1)
                GameInput.send(evade_key)
                self.assist_timer.restart()
                self.assist_timer.set_alarm(random.randint(2,4))
                self.assist_timer.start()

        if self.avatar_timer.alarmed():
            action_key = self.get_config_value('bandolier_avatar')
            GameInput.send(action_key)
            print(f"Performed action 'swap_to_avatar_weapons', sent key {action_key}")
            self.avatar_timer.reset()

    def action_toggle_assist(self, action_name, data):
        if action_name == 'assist_on':
            self.assist_timer.set_alarm(random.randint(2,4))
            self.assist_timer.start()
            self.assist_toggle = True
            print(f"Assist toggle ON")

        else:
            self.assist_toggle = False
            print(f"Assist toggle OFF")