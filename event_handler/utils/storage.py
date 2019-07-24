from threading import Lock
from copy import deepcopy

class Storage:
    def __init__(self):
        self._lock = Lock()
        self._storage = {}

    def get_data(self, key):
        with self._lock:
            data = self._storage.get(key)
            return deepcopy(data)

    def put_data(self, key, data):
        with self._lock:
            self._storage[key] = data
        