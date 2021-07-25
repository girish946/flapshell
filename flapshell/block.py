
from enum import Enum
class Type(Enum):
    INCLUDE = 0
    DEFINE  = 1
    COMMENT = 2

class Block:
    def __init__(self):
        self.type = None
        self.name = ""
        self.variables = {}
        self.functions = {}
        self.scopes = []
        self.text = ""