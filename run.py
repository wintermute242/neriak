import argparse, shutil, sys, os.path, threading, keyboard
import LogReader

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
    
    sys.exit(1)


# Set daemon flag so that new threads stop
# once the main thread calls system.exit().
reader = threading.Thread(target=
            LogReader(persona, queue).run,
            daemon=True
        )
        
agent = threading.Thread(target=
            Agent(persona, queue).run,
            daemon=True
        )
        
# Start execution of producer and consumer threads
# which will now run independently so long as the
# main thread is alive.
reader.start()
agent.start()
        
# Block until the hotkey combination is detected at which point the program exits
keyboard.wait('ctrl+shift+z')