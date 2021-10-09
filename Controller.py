from LogReader import LogReader
from Agent import Agent
import queue, threading, time

class Controller():
    """Coordinates setup of worker threads and shared memory objects."""
    def __init__(self, persona):
        self.queue  = queue.Queue()
        self.persona = persona
    
    def run(self):
        persona = self.persona
        queue = self.queue

        reader = threading.Thread(target=
                LogReader(persona, self.queue).run,
                daemon=True
            )
        
        agent = threading.Thread(target=
                Agent(persona, self.queue).run,
                daemon=True
            )
        
        reader.start()
        agent.start()
        
        # Go into an infinite loop and wait for the program to be terminated.
        try:
            while True:
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            reader.stop()
            agent.stop()