import queue, time, threading

class Agent:
    """Manages the player agent by listening for events and performing actions."""
    def __init__(self, persona, queue, sleep_time=0.1):
        self._queue   = queue
        self._persona = persona
        self._sleep_time = sleep_time

    def run(self):
        """Continuously check queue for new events and manage flow of executionm"""
        print(f"Thread[{threading.get_ident()}]: Agent has started...")
        
        # Looking for the main event loop handling triggered events? This is it.
        # The agent will continuosly check for triggered events and send them
        # to the persona to be handled in a first-in-first-out order.
        #
        # Either an event will be handled or, if there are no events, the agent
        # will temporarily go to sleep. After either of these cases complete the agent
        # will then be given an opportunity to update its state and do whatever other
        # work it needs to do.
        #
        # This is important as it allows the agent to build and maintain a more
        # complex internal state and respond to circumstances over a longer time horizon 
        # than reacting immediately to a single event. Things like measuring damage
        # taken over a certain interval, or doing a thing every n seconds might
        # be implemented in update(). It is a way to periodically return control of 
        # execution back to the persona to do whatever it needs to do.
        while True:
            try:
                event = self._queue.get(block=False)
                # Call on the persona to handle the event found
                #Agent._persona.process_event(event)

            except queue.Empty:
                time.sleep(self._sleep_time)
            
            finally:
                self.update_subscriptions()

    def update_subscriptions(self):
        pass