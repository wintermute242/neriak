import queue, time, sys

class Agent:
    def __init__(self, persona, queue):
        self.queue   = queue
        self.persona = persona

    def run(self):
        """Continuously check queue for new events"""
        print("The agent has started.")
        while True:
            try:
                event = self.queue.get()
                print(f"Got event from queue: {event.label}")
                self.persona.process_event(event)
            except queue.Empty:
                print("Nothing seen in queue")
                time.sleep(0.1)

    def stop(self):
        sys.exit()