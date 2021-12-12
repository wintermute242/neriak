from Neriak import *
import GameInput, Timer

class Cleric(Persona):
    # Initialize the superclass
    def __init__(self):
        super().__init__(name=__name__)
        self.pants_timer = Timer.Timer()
        self.pants_timer.set_alarm(11)

        # Accept group invite
        self.new_simple_action('accept_group', """(\w+) invites you to join a group.""", command=True)

        # Following
        self.new_simple_action('follow_on', """(\w+) tells (?:you|the group), 'follow me""", command=True)
        self.new_simple_action('follow_off', """(\w+) tells (?:you|the group), 'stop following""", command=True)
    
        # Potions/Pots
        self.new_simple_action('potion_instant_heal', """(\w+) tells (?:you|the group), '(instant heal potion)""", command=True)
        self.new_simple_action('potion_duration_heal', """(\w+) tells (?:you|the group), '(heal over time potion)""", command=True)

        # Auto follow after zone
        self.new_custom_action('follow_after_zoning',"""You have entered (.*)""", self.follow_after_zoning)
        self.zoning_follow_timer = Timer.Timer()
        self.zoning_follow_timer.set_alarm(self.get_config_value('follow_after_zoning_timer'))

    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Cleric()

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
            action_key = self.get_config_value('cast_pants')
            if (self.pants_timer.alarmed()):
                GameInput.send(action_key)
                print(f"Performed action 'cast pants', sent key {action_key}")
                self.pants_timer.restart()
                self.pants_timer.start()

        if self.zoning_follow_timer.alarmed():
            action_key = self.get_config_value('follow_on')
            GameInput.send(action_key)
            print(f"Just zoned. Following.")
            self.zoning_follow_timer.reset()

    def follow_after_zoning(self, action_name, data):
        """
        Starts a timer so that we can automatically start following after zoning.
        """
        self.zoning_follow_timer.start()
        print(f"Zoning timer set for {self.zoning_follow_timer.max_time_elapsed} seconds")
        print(f"Started: {self.zoning_follow_timer.timer_started}")
        print(f"Started at: {self.zoning_follow_timer.start_time}")
    
    def action_toggle_pants(self, action_name, data):
            if self.action_toggle_pants:
                self.action_toggle_pants = False
            else:
                action_key = self.get_config_value('cast_pants')
                GameInput.send(action_key)
                print(f"Performed action 'toggle_pants', sent key {action_key}")
                self.pants_toggle = True
                self.pants_timer.start()