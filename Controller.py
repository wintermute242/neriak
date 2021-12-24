import threading, queue, sys, time
from LogReader import LogReader
from Agent import Agent

class Controller():
    """
    Responsible for setting up the shared objects used for inter-thread
    communication and then creating the independent producer and consumer worker threads. 
    This is the 'main' thread which responds to user input like keyboard interrupts to 
    stop all execution.
    """
    def __init__(self, persona):
        self.queue  = queue.Queue()
        self.persona = persona

    def stop(self):
        self.reader._stop()
        self.agent._stop()
    
    def run(self):
        persona = self.persona
        queue = self.queue

        # Set daemon flag so that new threads stop
        # once the main thread calls system.exit().
        self.reader = threading.Thread(target=
                LogReader(persona, queue).run,
                daemon=True
            )
        
        self.agent = threading.Thread(target=
                Agent(persona, queue).run,
                daemon=True
            )
        
        # Start execution of producer and consumer threads
        # which will now run independently so long as the
        # main thread is alive.
        self.reader.start()
        self.agent.start()