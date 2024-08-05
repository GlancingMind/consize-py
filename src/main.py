#!/usr/bin/env python

import sys

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter
from Stack import Stack
from StackDeserializer import parse

def main():
    interpreter = Interpreter(
        ds=Stack(),
        cs=parse(sys.argv[1:]),
        maxRecursionDepth=0,
        trunkPrintOfStackToLength=50
    )
    CONSIZE_RULE_SET.apply(interpreter)
    print("Consize returns", interpreter.ds.toString())

if __name__ == "__main__":
    main()
