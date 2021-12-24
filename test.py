import logging, keyboard, threading
from Persona import Persona
from Controller import Controller

def hotkey_restart():
    global controller
    global persona
    logging.warning("Caught hotkey RESTART. Restarting.")
    controller.stop()
    controller = Controller(persona)
    controller.run()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%m/%d/%Y %I:%M:%S %p]')
persona = Persona('Monk')
controller = Controller(persona)
controller.run()

keyboard.add_hotkey('ctrl+shift+r', hotkey_restart)
keyboard.wait('ctrl+shift+x')

