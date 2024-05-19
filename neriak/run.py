from neriak.Neriak import Controller
import importlib
import argparse
import shutil
import sys
import os

def main():
    parser = argparse.ArgumentParser(description=
        'Implements a player agent for EverQuest by loading "Personas" defined as Python modules which define agent behavior to specified event triggers.'
        )
    parser.add_argument('-p', '--persona', dest='persona', type=str, help='Module name of the persona you wish to load, e.g. Healer.py')
    args = parser.parse_args()
    persona_name = "Default"

    if args.persona:
        persona_name = args.persona.lower().capitalize()

    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, 'neriak.ini')
    example_path = os.path.join(current_dir, 'example_neriak.ini')
    if not os.path.exists(config_path):
        if os.path.exists(example_path):
            print("No configuration file found. Creating copy from 'example_neriak.ini'")
            shutil.copyfile(example_path, config_path)
            print("Please setup 'neriak.ini' and run this program again.")
        else:
            print("No configuration file 'neriak.ini' or example file 'example_neriak.ini' was found.")
            print("Please create these files or download a new copy from the repo.")
        
        sys.exit(1)


    # Dynamically load the module specified on the command line. Assumes Module and Class name are the same.
    persona_module = 'neriak.' + persona_name
    module = importlib.import_module(persona_module)
    persona_class = getattr(module, persona_name)
    persona = persona_class()

    # Run the persona under a controller
    controller = Controller(persona)
    controller.run()