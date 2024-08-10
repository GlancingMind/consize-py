#!/usr/bin/env python

from Interpreter import Interpreter
from Stack import Stack
from StackParser import parse
import argparse

def main():
    parser = argparse.ArgumentParser(description="A stack rewrite system.")
    parser.add_argument("--trunk-print-length", type=int, default=50, help="Limits the length of status prints to x characters")
    parser.add_argument("-i", "--interactive", action="store_true", help="""Will run the interpreter in interactive mode. The user will have the option to step through each rule execution and some other niceties.""")
    parser.add_argument("-v", "--verbose", action="store_true", help="Starts verbose output. Will print chain of reasoning.")
    parser.add_argument("--native-words-dir", type=str, default="native-words", help="Set the directory from which native words should be loaded.")

    args, cs_args = parser.parse_known_args()

    interpreter = Interpreter(
        ds=Stack(),
        cs=parse((" ").join(cs_args)),
        native_rule_module_dir=args.native_words_dir,
        trunkPrintOfStackToLength=args.trunk_print_length,
        displayReasoningChain=args.verbose
    )
    interpreter.run(interactive=args.interactive)

    print("Result is:", interpreter.ds.toString(addEnclosingParenthesis=False))

if __name__ == "__main__":
    main()
