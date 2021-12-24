class Event:
    """
    When a Trigger is matched, an event is created which binds 
    the trigger name and the returned regex match object. Ideally
    the regex is designed so that the match groups contain specific
    values of interest for an action to respond to. This can be the
    name of a spell, a character, or the amount of damage taken or 
    healed.
    """
    def __init__(self, name, match, flag=None):
        """An object to encapsulate a task name and a regular expression match object."""
        self.name  = name
        self.match = match
        self.flag = flag