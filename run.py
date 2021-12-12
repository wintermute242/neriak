from Neriak import *
import argparse, shutil
import os.path

parser = argparse.ArgumentParser(description=
    'Implements a player agent for EverQuest by loading "Personas" defined as Python modules which define agent behavior to specified event triggers.'
    )
parser.add_argument('-p', '--persona', dest='persona', type=str, help='Module name of the persona you wish to load, e.g. Healer.py')
args = parser.parse_args()
persona_name = "Default"

if args.persona:
    persona_name = args.persona

if not os.path.exists('neriak.ini'):
    if os.path.exists('example_neriak.ini'):
        print("No configuration file found. Creating copy from 'example_neriak.ini'")
        shutil.copyfile('example_neriak.ini','neriak.ini')
        print("Please setup 'neriak.ini' and run this program again.")
    else:
        print("No configuration file 'neriak.ini' or example file 'example_neriak.ini' was found.")
        print("Please create these files or download a new copy from the repo.")
    
    os.exit(1)


# Dynamically load the module specified on the command line. Assumes Module and Class name are the same.
module = __import__(persona_name)
dynamic_persona = getattr(module, persona_name)
persona = dynamic_persona.load()

# Run the persona under a controller
controller = Controller(persona)
controller.run()