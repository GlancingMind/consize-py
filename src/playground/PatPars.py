# TODO führe : als Regel ein, so dass neue Regeln ins Regelwerk aufgenommen werden können.

import re

ruleset = [
    "#F #S @M #L | X Y -> @M | reverse #H concat",
    "#X #Y | swap -> #Y #X",
    "#X | dup -> #X #X",
    "#F | drop ->",
    "#X #Y #Z | rot -> #Z #X #Y",

    "#X #X | equal? -> t",
    "#X #Y | equal? -> f",

    "#X #X | identical? -> t",
    "#X #Y | identical? -> f",

    "emptystack -> [ ]",
    "[ ] #X | push -> [ #X ]",

    "[ #H @T ] | top -> #H",
    "[ ] | top -> nil",
    "nil | top -> nil",
]

def parse(ruleStr: str):
    lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
    ls = parseLeftRuleSide(lhs)
    rs = parseRightRuleSide(rhs)
    print(f"{ls} -> {rs}")

# Can parse a ruleside easiely by treating the whole words as a stack.
# At least the left side can be popped from continuesly until | is found, then
# the words are the callstack and everything after it is the datastack.
# The right side can be processed equally by treating the top of stack on the
# other side.
def parseLeftRuleSide(str: str):
    if str == "":
        return []

    tokens = re.split(r"\s+", str)

    appendRDS = True
    cs = []
    ds = []
    curStack = []
    while tokens != []:
        token = tokens.pop(0)
        if token == "|":
            ds = curStack
            curStack = []
        elif token == "[":
            curStack.append(parseStack(tokens))
        elif token != "":
            if appendRDS:
                appendRDS = not token.startswith('@')
            curStack.append(token)

    if cs == []:
        cs = curStack
    else:
        ds = curStack

    if appendRDS:
        ds = ["@RDS"] + ds

    return ds, cs

def parseRightRuleSide(str: str):
    tokens = re.split(r"\s+", str)

    appendRCS = True
    cs = []
    ds = []
    curStack = []
    while tokens != []:
        token = tokens.pop(0)
        if token == "|":
            ds = curStack
            curStack = []
        elif token == "[":
            curStack.append(parseStack(tokens))
        elif token != "":
            if appendRCS:
                appendRCS = not token.startswith('@')
            curStack.append(token)

    if ds == []:
        ds = curStack
    else:
        cs = curStack

    if appendRCS:
        cs.append("@RCS")

    return ds, cs

def parseStack(tokens: list):
    stack = []
    while tokens != []:
        token = tokens.pop(0)
        if token == "]":
            return stack
        elif token == "[":
            stack.append(parseStack(tokens))
        else:
            stack.append(token)

    return stack

for rule in ruleset:
    parse(rule)
