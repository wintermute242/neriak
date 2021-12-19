from Neriak import *
import Timer

class Default(Persona):
    #--> Initialize any persona specific variables here

    # Initialize the superclass
    def __init__(self, name=__name__):
        super().__init__(name)
        #--> Add setup here like triggers, actions, etc
        
        # Accept group invite
        self.new_simple_action('accept_group', """(\w+) invites you to join a group.""", command=True)

        # Following
        self.new_simple_action('follow_on', """(\w+) tells (?:you|the group), 'follow me""", command=True)
        self.new_simple_action('follow_off', """(\w+) tells (?:you|the group), 'stop following""", command=True)

        # Avatar proc
        self.new_custom_action('avatar', """Your body screams with the power of an Avatar""", self.action_avatar)
        self.avatar_timer = Timer.Timer()
        self.avatar_timer.set_alarm(230)

        # Potions/Pots
        self.new_simple_action('potion_instant_heal', """(\w+) tells (?:you|the group), '(instant heal potion)""", command=True)
        self.new_simple_action('potion_duration_heal', """(\w+) tells (?:you|the group), '(heal over time potion)""", command=True)

        # Auto follow after zone
        self.new_custom_action('follow_after_zoning',"""You have entered (.*)""", self.follow_after_zoning)
        self.zoning_follow_timer = Timer.Timer()
        self.zoning_follow_timer.set_alarm(self.get_config_value('follow_after_zoning_timer'))

        # Detect combat
        group_members = self.get_config_value('group_members').replace(',','|')
        if group_members:
            self.triggers.append(Trigger('in_combat',f"""(?:{group_members}).*for \d+ points of damage""", remote_timer=True, timer_max=5))
            self.actions.append(Action('in_combat', self.update_combat_status))
            self.in_combat = False
        
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        print(f"Instantiated class {__name__}")
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
        if self.zoning_follow_timer.alarmed():
            action_key = self.get_config_value('follow_on')
            GameInput.send(action_key)
            print(f"Just zoned. Following.")
            self.zoning_follow_timer.reset()

        # To support toggle actions, we need to continuously perform the action until otherwise
        # notified that it has succeeded. 
        for action in self.toggle.keys():
            if (self.toggle[action]):
                action_key = self.get_config_value(action)
                GameInput.send(action_key)
                print(f"Performed toggle action {action}")

    def action_avatar(self, action_name, data):
        """
        Triggered when the avatar proc is seen. Swaps back to primary
        weapon set until the avatar buff is a little over 2/3 done.
        """
        print(f"Avatar procced")
        action_key = self.get_config_value('bandolier_primary')
        GameInput.send(action_key)
        print(f"Performed action 'bandolier_primary', sent key {action_key}")
        self.avatar_timer.set_alarm(230)
        self.avatar_timer.start()

    def follow_after_zoning(self, action_name, data):
        """
        Starts a timer so that we can automatically start following after zoning.
        """
        self.zoning_follow_timer.start()
        print(f"Zoning timer set for {self.zoning_follow_timer.max_time_elapsed} seconds")
        print(f"Started: {self.zoning_follow_timer.timer_started}")
        print(f"Started at: {self.zoning_follow_timer.start_time}")

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


        

        
    
        
    