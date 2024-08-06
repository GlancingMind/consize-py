#!/usr/bin/env python

import sys

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter
from Stack import Stack
from StackParser import parse

# TODO add argparse
def main():
    interpreter = Interpreter(
        ruleset=CONSIZE_RULE_SET,
        ds=Stack(),
        cs=parse(sys.argv[1:]),
        maxRecursionDepth=0,
        trunkPrintOfStackToLength=50
    ).run(interactive=True)

    print("Result is:", interpreter.ds.toString())

if __name__ == "__main__":
    main()
