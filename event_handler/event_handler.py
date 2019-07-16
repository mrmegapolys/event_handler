from aggregator import EventAggregator
from threading import Thread

class EventHandler:
    def __init__(self):
        self.modules = {}
        self.actions = {}
        self.listeners = []
        self.data = {}
        self.config = None
        self.aggregator = EventAggregator()
        
    def add_listen_function(self, listener):#args
        self.listeners.append(listener)

    def _initialize_modules(self):
        pass

    def _start_listeners(self):
        for listener in self.listeners:
            thread = Thread(target=listener, daemon=True)
            thread.start()

    def configure(self, conf_file):
        pass

    def start(self):
        if not self.config:
            raise NotImplementedError('Please configure EventHandler first')
        self._initialize_modules()
        self._start_listeners()

        while True:
            event = self.aggregator.get_event()
            actions = self.actions[event]
            for action in actions:
                action()


