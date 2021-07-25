import abc
class Parser:
    def __init__(self, debug=True, scope=None):
        self.debug = debug
        self.scope = scope

    @abstractmethod
    def parse(self, code):
        pass
