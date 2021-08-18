#!/usr/bin/env python3

import os
import sys
import argparse
import re
from .block import Block


def iterator(code):

    start_blk = { "{":"}","(":")", "[":"]"}

    stmt = ""
    comment_or_string = False
    blocks = []
    blk = Block()
    current_blk = blk
    blk_type = []
    blocks.append(blk)
    for i in range(len(code)):
        stmt = stmt+code[i]

        if (code[i] == '"' or code[i] == "'"):
            #print("stmt: ", stmt)
            if (not comment_or_string):
                comment_or_string = True
            else:
                if (code[i-1] == "\\"):
                    pass
                else:
                    comment_or_string = False
        if (comment_or_string):
            pass
            """" elif( code[i] == ';'):
            print("Statement ", "    "+stmt)
            blocks[-1].text = blocks[-1].text+ stmt
            stmt = "" """
        elif (code[i] == "#"):
            if(code[i+1:].find("include") == 0):

                print("include found")
                line = code[i:].find(">")
                stmt = stmt+code[i+1:line]
                print("include: --- ", stmt)

                blocks[-1].text = blocks[-1].text + stmt
                stmt = ""
                i = line

            elif(code[i+1:].find("define") == 0):
                print("define macro found")
            elif(code[i+1:].find("ifndef") == 0):
                print("ifdef found")

        elif code[i] in start_blk:
            blk_type.append( code[i])
            print("blk_type:",blk_type)
            #print("comment_or_string: ", comment_or_string)
            blocks.append(Block())

        elif(blk_type)and  (start_blk[blk_type[-1]] == code[i]):
            #while code[i]:
            blk_type.pop(-1)
            blocks[-1].text = blocks[-1].text + stmt
            stmt = ""
            print("blk-----", blk_type)

    print(len(blocks), blocks)
    for i in blocks:
        if i.text:
            print("start: ---", i)
            print("end: ---")

def fix_strings(code):

    code = re.sub(r"\\\"", "  ", code)
    code = re.sub(r"\\\'", "  ", code)
    strings = re.findall(r'".*?"',  code)

    for i in strings:
        code = code.replace(i, '"'+(" "*(len(i)-2))+'"')
    #print(code)
    return code


def remove_comments(code):
    sep='\n'
    code = code.replace('\n', " \n")
    code = re.sub(r'/\*.*?\*/', r'', code, flags=re.MULTILINE | re.DOTALL)
    code = re.sub(r"\/\/[^\n\r]+?(?:\*\)|[\n\r])", " ", code)
    code = re.sub(r'\\\n', r' ', code, flags=re.MULTILINE | re.DOTALL)

    return code

def fix_includes(code):

    code = re.sub(r'#\s*include\s*', '#include', code)
    fix_includes = re.compile(r'#include["<]?([^">]+)[">]?')

    includes = re.findall(fix_includes, code)
    for i in includes:
        code = re.sub(fr'#include["<]?([^">]{i})[">]?', fr'#include<{i}>', code)
        code = re.sub(fr'#include"{i}"', fr"#include<{i}>", code)

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
    code = re.sub(r'#\s+', '#', code)
    code = fix_includes(code+";")
    code = fix_strings(code)
    code = remove_comments(code)
    # print(code)
    iterator(code)


def read_code(file_name):
    return open(file_name).read()

