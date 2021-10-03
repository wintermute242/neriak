class Persona:
    """A persona encapsulates the logic behind how a character will be played. Two personas might play the same class very differently depending on the desired goal."""
    def __init__(self, name, log_file_path):
        self.name = name
        self.log_file_path = log_file_path
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.label] = task

    def get_tasks(self):
        return self.tasks.values()

    def get_task_by_label(self, name):
        return self.tasks[name]

    def process_event(self, event):
        data = event.match
        task = self.get_task_by_label(event.label)
        task.execute(data)
    
