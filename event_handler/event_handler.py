from aggregator import EventAggregator
from storage import Storage
from threading import Thread
from configparser import ConfigParser
import modules

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
        pass

    def _initialize_modules(self):
        for module_name in self.modules_config.sections():
            module_config = self.modules_config[module_name]
            if module_config.getboolean('enabled'):
                module_class = eval('modules.' + module_name)
                module = module_class(module_config)
                self.modules[module_name] = module

    def _start_threaded(self):
        pass

    def start(self, modules_config_filepath, user_config_filepath=None):
        self.modules_config = ConfigParser()
        self.modules_config.read(modules_config_filepath)
        if user_config_filepath:
            self.user_config = ConfigParser()
            self.user_config.read(user_config_filepath)

        self._initialize_modules()
        """
        while True:
            event = self.aggregator.get_event()
            actions = self.actions[event]
            for action in actions:
                action()
        """


