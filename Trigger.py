import re
class Trigger:
    """An object encapsulating a regex and a trigger name."""
    def __init__(self, name, regex):
        self.name  = name
        self.regex = re.compile(regex)