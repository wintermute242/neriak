class Action:
    def __init__(self, name):
        self.name = name
        self.sequence = []

    def add_sequence_item(self, func):
        """Take a function and appends it to a list of items to be executed."""
        self.sequence.append(func)

    def execute(self, data):
        for item in self.sequence:
            item(data)