class Event:
    def __init__(self, trigger, match):
        """An object to encapsulate a name and a regular expression match."""
        self.trigger = trigger
        self.match = match