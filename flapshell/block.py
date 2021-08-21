
import json
from enum import Enum
class Type(Enum):
    INCLUDE = 0
    DEFINE  = 1
    COMMENT = 2

class Block:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

        self.type = None
        self.variables = {}
        self.text = ""
        self.children = []

    def dump(self):
        parent_name = ""
        text_data = self.text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
        if self.parent:
            parent_name = self.parent.name

        string = f'{{ "name":"{self.name}", "parent": "{parent_name}", "text":"{text_data}", "children":['
        for index, i in enumerate(self.children):
            string+= i.dump()
            if not (i is self.children[-1] ):
                string+= ","
        string+= ']}'
        #print(string)
        return string

    def __str__(self):
        return repr(self)


    def __repr__(self):
        dicts = json.loads(self.dump())
        return json.dumps(dicts, indent=1)

    def parse(self, code, loc):
        print(code[loc])
        blk_type = code[loc]

