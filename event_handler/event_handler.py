from threading import Thread
from configparser import ConfigParser
from copy import deepcopy

from .aggregator import EventAggregator
from .storage import Storage
from . import modules

class EventHandler:
    def __init__(self):
        self.modules = {}
        self.actions = {}
        self.threaded_functions = []
        self.storage = Storage()
        self.user_config = None
        self.modules_config = None
        self.aggregator = EventAggregator()
        
    def add_threaded_function(self, function):
        self.threaded_functions.append(function)

    def register_action(self, event_type, action):
        if not self.actions.get(event_type):
            self.actions[event_type] = []
        self.actions[event_type].append(action)

    def _initialize_modules(self):
        for module_name in self.modules_config.sections():
            module_config = self.modules_config[module_name]
            if module_config.getboolean('enabled'):
                module = modules.__dict__[module_name](module_config)
                self.modules[module_name] = module

    def _start_threaded(self):
        for function in self.threaded_functions:
            thread = Thread(target=function,
                            args=(self.modules, self.storage, deepcopy(self.user_config), self.aggregator),
                            daemon=True)
            thread.start()

    def start(self, modules_config_filepath, user_config_filepath=None):
        self.modules_config = ConfigParser()
        self.modules_config.read(modules_config_filepath)
        if user_config_filepath:
            self.user_config = ConfigParser()
            self.user_config.read(user_config_filepath)

        self._initialize_modules()
        self._start_threaded()

        while True:
            event = self.aggregator.get_event()
            actions = self.actions[event.type]
            for action in actions:
                action(self.modules, self.storage, deepcopy(self.user_config), event)
