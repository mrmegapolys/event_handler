class BaseEvent:
    def __init__(self, data):
        self.data = data
        self.type = self.__class__.__name__
        if self.type == 'BaseEvent':
            raise NotImplementedError