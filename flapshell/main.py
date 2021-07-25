#!/usr/bin/env python3

import os
import sys
import argparse
import re


def remove_comments(code):
    sep='\n'
    code = code.replace('\n', " \n")
    code = re.sub(r"\/\/[^\n\r]+?(?:\*\)|[\n\r])", ";", code)
    code = re.sub(r'/\*.*?\*/', r'', code, flags=re.MULTILINE | re.DOTALL)
    code = re.sub(r'\\\n', r' ', code, flags=re.MULTILINE | re.DOTALL)

    return code

def fix_includes(code):
    code = re.sub(r'#\s*include\s*', '#include', code)

    fix_includes = re.compile(r'#include["<]?([^">]+)[">]?')
    includes = re.findall(fix_includes, code)
    print(includes)
    for i in includes:
        code = re.sub(fr'#include["<]?([^">]{i})[">]?', fr'#include<{i}>;', code)
    return code


def parse_c(code):
    """
    This method should
    1. Fix include statements
    2. Fix comments
    3. insert apt delimiters for eol
    4. parse all blocks
    5. define scopes
    """
    print(type(code))
    #code = re.sub(r'#\s+', '#', code)
    code = fix_includes(code)
    code = remove_comments(code)

    print(code)


def read_code(file_name):
    return open(file_name).read()


