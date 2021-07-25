import parser
import re

class BlockParser(parser.Parser):

    def __init__(self, debug=False, scope=None):
        self.debug = debug
        self.scope = scope

    def parse(self, code):
        print("block parsing for :", code)

