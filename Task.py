class Task:
    def __init__(self, label, trigger, actions):
        self.label   = label
        self.actions = []
        self.trigger = trigger
        for action in actions:
            self.actions.append(action)

    def execute(self, data):
        for action in self.actions:
            action.execute(data)