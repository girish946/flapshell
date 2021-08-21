#!/usr/bin/env python3

import os
import sys
import argparse
import re
from .block import Block

def set_text_to_parent(blk, stmt):
    temp_blk = blk
    blk.text += stmt
    while temp_blk.parent:
        temp_blk.text += stmt
        temp_blk = temp_blk.parent

def iterator(code):

    start_blk = { "{":"}","(":")", "[":"]"}

    stmt = ""
    comment_or_string = False
    blocks = []
    blk = Block("global")
    current_blk = blk
    blk_type = []
    blocks.append(blk)
    last_stmt = 0
    blk_count = 0

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
        elif( code[i] == ';'):
            #print("Statement ", "    "+stmt)
            #blocks[-1].text = blocks[-1].text+ stmt
            #stmt = ""
            last_stmt = i

        elif (code[i] == "#"):
            if(code[i+1:].find("include") == 0):

                #print("include found")
                line = code[i:].find(">")
                stmt = stmt+code[i+1:line]
                #print("include: --- ", stmt)

                blocks[-1].text = blocks[-1].text + stmt
                stmt = ""
                i = line
                last_stmt = i

            elif(code[i+1:].find("define") == 0):
                #print("define macro found")
                pass
            elif(code[i+1:].find("ifndef") == 0):
                #print("ifdef found")
                pass

        elif code[i] in start_blk:
            blk_type.append( code[i])
            #print("blk_type:",blk_type)
            #print(last_stmt, i ,"the block name-----", code[last_stmt:i], "------.....")
            #print("comment_or_string: ", comment_or_string)
            #if blk_type:
            blk_name = code[last_stmt+1:i].strip().replace("\n", "").replace("'", "\\'").replace('"','\\"')
            #print("blk_name", [blk_name])
            last_stmt = i
            current_blk.children.append(Block(blk_name,parent=current_blk) )
            current_blk = current_blk.children[-1]
            #else:
            #    blocks.append(Block())
            #    current_blk = blocks[-1]

        elif(blk_type)and  (start_blk[blk_type[-1]] == code[i]):
            blk_type.pop(-1)
            set_text_to_parent(current_blk, stmt)
            blk.text+= stmt
            #current_blk.text = current_blk.text + stmt
            stmt = ""
            #print(current_blk)
            if blk_type:
                if current_blk.children:
                    current_blk = current_blk.children[-1].parent
            else:
                current_blk = blk
            #print("blk-----", blk_type)
            #if blk_type:
    print(blk)
    """print("\n\n\n\n", len(blocks), blocks)
    for i in blocks:
        if i.text:
            print("start: ---\n", i)
            print("end: ---")"""

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
    #print(type(code))
    code = re.sub(r'#\s+', '#', code)
    code = fix_includes(code+";")
    code = fix_strings(code)
    code = remove_comments(code)
    # print(code)
    iterator(code)


def read_code(file_name):
    return open(file_name).read()

