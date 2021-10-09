class Event:
    def __init__(self, task_label, match):
        """An object to encapsulate a task label and a regular expression match."""
        self.label  = task_label
        self.match  = match