from Neriak import *
from Default import Default
import GameInput, Timer, random

class Ranger(Default):
    # Initialize the superclass
    def __init__(self):
        super().__init__(name=__name__)
        #--> Add setup here like triggers, actions, etc

    
    def load():
        """Returns a new instance of the class. This should match the class name."""
        return Ranger()

    def update(self):
        """
        Any long term state can be maintained here. This will get called so that flow of 
        execution can be periodically returned to the player persona. The amount of time between
        calls is a either the time needed to process a particular event or the sleep_time
        parameter passed to Agent.
        """
        super().update()
        print("Ran Ranger.update()")