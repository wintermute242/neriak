import argparse, shutil, sys, os.path, threading, keyboard, logging, queue
from LogReader import LogReader
from Agent import Agent

def get_args():
    parser = argparse.ArgumentParser(description=
        'Implements a player agent for EverQuest by loading "Personas" defined as Python modules which define agent behavior to specified event triggers.'
        )
    parser.add_argument('-p', '--persona', dest='persona', type=str, help='Module name of the persona you wish to load, e.g. Healer.py')
    parser.add_argument('-l', '--log-level', dest='log_level', type=str, help='Set the logging level, e.g. DEBUG, INFO, WARNING, ERROR, or CRITICAL')
    return parser.parse_args()

def check_config_exists():
    if not os.path.exists('neriak.ini'):
        if os.path.exists('example_neriak.ini'):
            logging.error("No configuration file found. Creating copy from 'example_neriak.ini'")
            shutil.copyfile('example_neriak.ini','neriak.ini')
            logging.error("Please setup 'neriak.ini' and run this program again.")
        else:
            logging.error("No configuration file 'neriak.ini' or example file 'example_neriak.ini' was found.")
            logging.error("Please create these files or download a new copy from the repo.")
    
        sys.exit(1)

def hotkey_exit():
    logging.warning("Caught hotkey EXIT. Exiting program")
    sys.exit(0)

def hotkey_restart():
    logging.warning("Caught hotkey RESTART. Restarting.")
    # TODO: Restart the program somehow


# Main entry point

persona_name = "Default"
logging_level = None
args = get_args()

# Handle arguments
if args.persona:
    persona_name = args.persona

if args.logging_level:
    if args.logging_level in ['INFO','WARNING','DEBUG','ERROR','CRITICAL']:
        logging_level = args.logging_level
    else:
        print(f"Logging level '{args.logging_level}' is not recognized. Using default value of 'WARNING'.")

# Basic setup and sanity checks
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%m/%d/%Y %I:%M:%S %p]', level=args.logging_level or logging.WARNING)
check_config_exists()

# Start threads
# Set daemon flag so that new threads stop
# once the main thread calls system.exit().
queue = queue.queue()

reader = threading.Thread(target=
            LogReader(persona_name, queue).run,
            daemon=True
        )
        
agent = threading.Thread(target=
            Agent(persona_name, queue).run,
            daemon=True
        )
        
# Start execution of producer and consumer threads
# which will now run independently so long as the
# main thread is alive.
reader.start()
agent.start()

keyboard.add_hotkey('ctrl+shift+r', hotkey_restart)
keyboard.wait('ctrl+shift+x')
