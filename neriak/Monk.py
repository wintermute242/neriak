from neriak.Neriak import Persona, Action, Trigger
from neriak.util.timer import Timer
from neriak.util import GameInput
import random

class Monk(Persona):
    # Initialize the superclass
    def __init__(self):
        super().__init__(name=__name__)
        self.assist_toggle = False
        self.assist_timer = Timer()
        self.assist_timer.set_alarm(2)
        self.avatar_timer = Timer()
        self.avatar_timer.set_alarm(230)

        # Accept group invite
        self.new_simple_action('accept_group', """(\w+) invites you to join a group.""", command=True)

        # Following
        self.new_simple_action('follow_on', """(\w+) tells (?:you|the group), 'follow me""", command=True)
        self.new_simple_action('follow_off', """(\w+) tells (?:you|the group), 'stop following""", command=True)

        # Avatar proc
        self.new_custom_action('avatar', """Your body screams with the power of an Avatar""", self.action_avatar)
        self.avatar_timer = Timer()
        self.avatar_timer.set_alarm(self.get_config_value('avatar_swap_timer'))

        # Assist
        self.new_custom_action('assist_on', """(\w+) tells (?:you|the group), '(assist me)""", 
            self.action_toggle_assist, command=True)
        self.new_custom_action('assist_off', """(\w+) tells (?:you|the group), '(stop assisting)""", 
            self.action_toggle_assist, command=True)
        self.assist_toggle = False
        self.assist_timer = Timer()
        self.assist_timer.set_alarm(2)

        # DPS burn
        self.new_simple_action('disc_burn', """(\w+) tells (?:you|the group), '(burn)""", command=True)
        
        # Potions/Pots
        self.new_simple_action('potion_instant_heal', """(\w+) tells (?:you|the group), '(instant heal potion)""", command=True)
        self.new_simple_action('potion_duration_heal', """(\w+) tells (?:you|the group), '(heal over time potion)""", command=True)

        # Auto follow after zone
        self.new_custom_action('follow_after_zoning',"""You have entered (.*)""", self.follow_after_zoning)
        self.zoning_follow_timer = Timer()
        self.zoning_follow_timer.set_alarm(self.get_config_value('follow_after_zoning_timer'))
        
        # Dark elf mask
        self.new_simple_action('dark_elf_mask', """(\w+) tells (?:you|the group), '(mask up)""", command=True)

        # Feign death
        self.new_simple_action('feign_death', """(\w+) tells (?:you|the group), '(flop)""", command=True)

        # Mend
        self.new_simple_action('mend', """(\w+) tells (?:you|the group), '(mend)""", command=True)

        # Detect combat
        group_members = self.get_config_value('group_members').replace(',','|')
        self.triggers.append(Trigger('in_combat',f"""(?:{group_members}).*for \d+ points of damage""", remote_timer=True, timer_max=5))
        self.actions.append(Action('in_combat', self.update_combat_status))
        self.in_combat = False
    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Monk()

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

        if self.avatar_timer.alarmed():
            action_key = self.get_config_value('bandolier_avatar')
            GameInput.send(action_key)
            print(f"Performed action 'swap_to_avatar_weapons', sent key {action_key}")
            self.avatar_timer.reset()


        if self.zoning_follow_timer.alarmed():
            action_key = self.get_config_value('follow_on')
            GameInput.send(action_key)
            print("Just zoned. Following.")
            self.zoning_follow_timer.reset()



    def action_avatar(self, action_name, data):
        print("Avatar procced")
        action_key = self.get_config_value('bandolier_primary')
        GameInput.pause(0.2)
        GameInput.send(action_key)
        print(f"Performed action 'bandolier_primary', sent key {action_key}")
        self.avatar_timer.set_alarm(230)
        self.avatar_timer.start()

    def action_toggle_assist(self, action_name, data):
        if action_name == 'assist_on':
            self.assist_timer.set_alarm(random.randint(2,4))
            self.assist_timer.start()
            self.assist_toggle = True
            print("Assist toggle ON")

        else:
            self.assist_toggle = False
            print("Assist toggle OFF")

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