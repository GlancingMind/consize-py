# TODO Erlaube [ 1 2 3 4 5 ] [ #F #S @M #L ]
# TODO vereinfache die stack annotationen noch weiter, so dass | nicht notwendig ist.
# TODO fuhre : als regel ein, so dass neue Regeln ins Regelwekr aufgenommen werden können.

import re

ruleset = [
    "#F #S @M #L -> @M"
    "#X #Y | swap -> #Y #X",
    "#X | dup -> #X #X",
    "#F | drop -> ",
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
    "-rot -> rot rot rot"
]

def parse(ruleStr: str):
    lhs, *rhs = re.split(r"\s*->\s*", ruleStr, 1)
    ls = parseRuleSide(lhs)
    rs = parseRuleSide(rhs)
    print(ls)
    print(rs)

# Can parse a ruleside easiely by treating the whole words as a stack.
# At least the left side can be popped from continuesly until | is found, then
# the words are the callstack and everything after it is the datastack.
# The right side can be processed equally by treating the top of stack on the
# other side.
def parseRuleSide(str: str):
    tokens = re.split(r"\s+", str)
    cs = []
    ds = []
    curStack = []
    while tokens != []:
        token = tokens.pop()
        if token == "|":
            cs = ds
            ds = []
        elif token == "]":
            newStk = []
            ds += newStk
            curStack = newStk
        elif token == "[":
            tmp = ds.pop()
            ds += curStack
            curStack = tmp
        else:
            curStack += token


for rule in ruleset:
    parse(rule)
