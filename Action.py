import Timer

class Action:
    """
    Designed to encapsulate everything needed for implementing an action.

    Action types:

        Simple - Every trigger event will *always* cause an action. 
                 Be careful, a lot of events can build up if your triggers
                 occur too frequently.

        Timed  - Every trigger event will cause an action so long as enough time has
                 passed since the last action completed.

        Toggle - Has separate triggers for events which toggle the action on and off.
                 Once toggled on, this action automatically occurs at a regular set
                 interval until toggled off.
    """
    def __init__(self, name, toggled_action=False, ini_label=None):
        self.name = name
        # By default the label in the INI will be the same as the action name
        self.ini_label = name
        if ini_label:
            self.ini_label = ini_label
        self.toggled_action = toggled_action
        self.toggled_on = False
        self.toggle_timer = Timer.Timer()
        # Contain all  the regexes that trigger the action or toggle it on/off
        self.toggle_on_triggers = []
        self.toggle_off_triggers = []
        # Compared to timer to determine if enough time has passed to 
        # perform the action again.
        self.time_last_action_completed = None

    def trigger(self):


    def add_trigger(self, trigger):
        self.toggle_on_triggers.append(trigger)

    def get_triggers(self, ):

    def add_toggle_on_trigger(self, trigger):
        self.toggle_on_triggers.append(trigger)

    def add_toggle_off_trigger(self, trigger):
        self.toggle_off_triggers(trigger)

    def set_toggle_timer(self, seconds):
        """
        The number of seconds this action is on 'cooldown'
        """
        self.toggle_timer.set_alarm(seconds)
