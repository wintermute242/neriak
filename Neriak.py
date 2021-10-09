import os
from Persona import Persona
from Controller import Controller
from Action import Action
from Task import Task
from Trigger import Trigger

log_dir = os.path.join('F:', 'Games', 'Daybreak Game Company', 'Installed Games', 'EverQuest', 'Logs')
log_name = 'eqlog_Ashtoroth_thornblade.txt'
log_path = os.path.join(log_dir, log_name)
persona = Persona('tracker',log_path)

action = Action('print_line')
action.add_sequence_item(
    lambda line: print(line.group(0), flush=True)
    )
trigger = Trigger('capture_whole_line','(.+)')
actions = [action]
t = Task('print_line',trigger,actions)
persona.add_task(t)

controller = Controller(persona)
controller.run()