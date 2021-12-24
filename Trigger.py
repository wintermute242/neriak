import re

class Trigger:
    """
    A named regex which when matched triggers an event. 
    This is will be matched against every incoming line from log files.
    """
    def __init__(self, name, regex, remote_timer=False, timer_max=0, flag=None):
        self.name  = name
        self.regex = re.compile(regex, re.IGNORECASE)
        self.remote_timer = remote_timer
        self.remote_timer_max = timer_max
        self.flag = flag