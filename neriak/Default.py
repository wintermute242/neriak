from neriak.Neriak import Persona

class Default(Persona):
    #--> Initialize any persona specific variables here

    # Initialize the superclass
    def __init__(self):
        super().__init__('Default')
        #--> Add setup here like triggers, actions, etc


    def update(self):
        """
        Any long term state can be maintained here. This will get called so that flow of 
        execution can be periodically returned to the player persona. The amount of time between
        calls is a either the time needed to process a particular event or the sleep_time
        parameter passed to Agent.
        """
        # This gets called roughly every tenth of a second by default. You can do this like
        # check timers to see how much time has elapsed, and take actions if necessary.

        
    
        
    