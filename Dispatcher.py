from LogReader import LogReader
from Agent import Agent
import queue, threading, time

class Dispatcher():
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
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            reader.stop()
            agent.stop()