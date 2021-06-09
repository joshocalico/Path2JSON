"""
A very naive path definition (set) to JSON converter
"""

import sys
import json

from bs4 import BeautifulSoup

# Operations

def basic_op(tokens: list):
    op = tokens.pop(0)
    if "," in op:
        return op.split(",")
    else:
        # Space co-ord?
        return [op, tokens.pop(0)]

def no_op(_: list):
    return 0

def arc_op(tokens: list):
    return [
        basic_op(tokens),
        tokens.pop(0),
        tokens.pop(0),
        tokens.pop(0),
        basic_op(tokens),
    ]

# Whitelist

def new_op(tokens: list):
    if tokens[0] in ["M", "C", "A", "Q", "L", "Z"]:
        return tokens.pop(0)

### Actual logic

def path_to_json(path: str):
    def_list = path.split(" ")
    result_list = []
    current_op = ''
    op_actions = []
    while def_list:
        next_token = def_list[0]
        is_opcode = new_op(def_list)

        if not is_opcode and not current_op:
            print("Panic! Expected opcode, got", next_token)
            print(is_opcode, current_op)
            raise ValueError

        if is_opcode:
            if current_op != is_opcode:
                if current_op:
                    result_list.append([ current_op, op_actions ])
                op_actions = []
                current_op = is_opcode

        if current_op == 'A':
            strategy = arc_op
        elif current_op == "Z":
            strategy = no_op
        else:
            strategy = basic_op

        try:
            op_actions.append(strategy(def_list))

        except IndexError:
            print("Failed", current_op)
            print("At parse of", next_token)
            break

    result_list.append([ current_op, op_actions ])
    return result_list

def do_convert():
    with open(sys.argv[1]) as xml:
        root = BeautifulSoup(xml, "xml")
    path_elements = root.find_all("path")
    svg_json = []
    print("Found", len(path_elements), "path(s)")
    for path in path_elements:
        try:
            svg_json.append(path_to_json(path["d"]))
        except AttributeError:
            print("Path at index", len(svg_json), "has no 'd' (Definition) attribute. Skipping.")
    with open(sys.argv[2], "w") as w:
        w.write(json.dumps(svg_json, separators=(',', ':')))
    print("Output complete!")

try:
    do_convert()

except IndexError:
    print("""Usage:
    python path_json[.py] <filename>
    Expected filename, none provided.""")

except FileNotFoundError:
    print("No such file!")
