#!/usr/bin/env python

import sys
from Interpreter import Interpreter
from RuleSet import RuleSet
from Stack import Stack
from StackParser import parse
import argparse

def main():
    parser = argparse.ArgumentParser(description="A stack rewrite system.")
    parser.add_argument("--ruleset", type=str, help="Load a ruleset from some file")
    parser.add_argument("--trunk-print-length", type=int, default=50, help="Limits the length of status prints to x characters")
    parser.add_argument("-i", "--interactive", action="store_false", help="""Will run the interpreter in interactive mode. The user will have the option to step through each rule execution and some other niceties.""")
    parser.add_argument("-v", "--verbose", action="store_true", help="Starts verbose output. Will print chain of reasoning.")

    args, cs_args = parser.parse_known_args()

    ruleset = RuleSet([])
    try:
        ruleset = RuleSet.load(args.ruleset)
    except FileNotFoundError as e:
        print(f"Could not find {args.ruleset}, exiting...", file=sys.stderr)
        return 1

    interpreter = Interpreter(
        ruleset=ruleset,
        ds=Stack(),
        cs=parse((" ").join(cs_args)),
        trunkPrintOfStackToLength=args.trunk_print_length,
        displayReasoningChain=args.verbose
    )
    interpreter.run(interactive=args.interactive)

    print("Result is:", interpreter.ds.toString(addEnclosingParenthesis=False))

if __name__ == "__main__":
    main()
