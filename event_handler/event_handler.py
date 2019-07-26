from threading import Thread
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from io import StringIO

from .utils import EventAggregator, Storage
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

    def register_action(self, event_class, action):
        event_name = event_class.__name__
        self.actions.setdefault(event_name, [])
        self.actions[event_name].append(action)

    def start(self, modules_config_filepath, user_config_filepath=None, max_workers=1):
        self._init(modules_config_filepath, user_config_filepath)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                event = self.aggregator.get_event()
                actions = self.actions[event.__class__.__name__]
                executor.submit(self._run_actions, event, actions)

#------------------------------------------------

    def _get_user_config(self):
        config_string = StringIO()
        self.user_config.write(config_string)
        config_string.seek(0)
        config_copy = ConfigParser()
        config_copy.read_file(config_string)
        return config_copy

    def _initialize_modules(self):
        for module_name in self.modules_config.sections():
            module_config = self.modules_config[module_name]
            if module_config.getboolean('enabled'):
                module = modules.__dict__[module_name](module_config)
                self.modules[module_name] = module

    def _start_threaded(self):
        for function in self.threaded_functions:
            user_config = self._get_user_config()
            thread = Thread(target=function,
                            args=(self.modules, self.storage, user_config, self.aggregator),
                            daemon=True)
            thread.start()

    def _run_actions(self, event, actions):
        for action in actions:
            user_config = self._get_user_config()
            action(self.modules, self.storage, user_config, event)

    def _init(self, modules_config_filepath, user_config_filepath):
        self.modules_config = ConfigParser()
        self.modules_config.read(modules_config_filepath)
        if user_config_filepath:
            self.user_config = ConfigParser()
            self.user_config.read(user_config_filepath)

        self._initialize_modules()
        self._start_threaded()
