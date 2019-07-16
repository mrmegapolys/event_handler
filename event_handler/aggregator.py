from queue import Queue

class EventAggregator:
    def __init__(self):
        self._event_queue = Queue()

    def put_event(self, event):
        self._event_queue.put(event)

    def get_event(self):
        return self._event_queue.get()
    