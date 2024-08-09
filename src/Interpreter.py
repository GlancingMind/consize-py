import importlib
import importlib.util
import os
from sys import stderr
import sys
from Rule import NativeRule
import RuleParser as RuleParser
from RuleSet import RuleSet
from Stack import Stack
import StackParser
from TerminalEscsapeCodes import TerminalEscapeCodes as TEC

class Interpreter:

    def __init__(self,
            ruleset = RuleSet([]),
            cs = Stack(),
            ds = Stack(),
            native_rule_module_dir = "",
            trunkPrintOfStackToLength = 0,
            displayReasoningChain = True
        ):
        self.ds = ds
        self.cs = cs
        self.trunkPrintOfStackToLength = trunkPrintOfStackToLength
        self.displayReasoningChain = displayReasoningChain
        self.native_rule_module_dir = native_rule_module_dir
        self.ruleset = ruleset
        self.native_rules = RuleSet([])
        if self.native_rule_module_dir:
            self.discover_native_rules()
        self.halt = False

    def halt(self):
        self.halt = True

    def run(self, interactive=False):
        while not self.halt:
            if self.displayReasoningChain:
                self.log_state()
            try:
                if interactive:
                    # TODO use readline instead of input for history and autocompletion
                    user_input = input("Enter '?' for help:\n> ").strip()
                    if user_input == "":
                        # When user only pressed enter or only whitespace, then do a single step
                        self.make_step()
                        continue
                else:
                    self.continue_to_end()
                    self.halt()
            except EOFError:
                break

            # No interpreter command given, treat input as data to call-/datastack
            self.cs = Stack(*StackParser.parse(user_input), *self.cs)
            self.make_step()
            # TODO if a word is unknown, call read-word, which will move the word
            # over to the datastack. Add an noop read-word impl.
            # Or add a some callback mechanismn, which a plugin could register for (observer).

    def make_step(self):
        some_rule_applied = False
        for rule in self.ruleset:
            if rule.execute(interpreter=self):
                some_rule_applied = True
                break
        for rule in self.native_rules:
            if rule.execute(interpreter=self):
                some_rule_applied = True
                break

        if not some_rule_applied:
            # If word wasn't found, move it from the callstack to the datastack
            if self.cs != []:
                wrd, *rcs = self.cs
                self.ds.append(wrd)
                self.cs = Stack(*rcs)

        return some_rule_applied

    def make_steps_until_unknown_word(self):
        while self.make_step():
            pass
        self.print_error(f"No applicative rules found. Unknown word encountered.")

    def continue_to_end(self):
        while not self.cs == []:
            self.make_step()

    def log_state(self):
        datastack=self.ds.toString(addEnclosingParenthesis=False, trunkLength=self.trunkPrintOfStackToLength)
        callstack=self.cs.toString(addEnclosingParenthesis=False, trunkLength=self.trunkPrintOfStackToLength, tosIsLeft=True)
        step =f"{datastack} {TEC.RED}{TEC.BOLD}|{TEC.END} {TEC.BLUE}{callstack}{TEC.END} {TEC.BOLD}{TEC.RED}-->{TEC.END}"
        self.print(step)

    def print_error(self, msg: str):
        print(f"{TEC.RED}{TEC.BOLD}{msg}{TEC.END}", file=stderr)

    def print_warning(self, msg: str):
        print(f"{TEC.YELLOW}{TEC.BOLD}{msg}{TEC.END}", file=stderr)

    def print(self, msg: str):
        print(msg, file=stderr)

    def discover_native_rules(self):
        # TODO does this also remove modules, which are no longer available?
        # TODO should return error, the calle should handle printing of errors
        rs = RuleSet([])
        try:
            for module_name in os.listdir(self.native_rule_module_dir):
                module_path = os.path.join(self.native_rule_module_dir, module_name)
                if not os.path.isfile(module_path):
                    continue

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is None:
                    self.print_error(f"Cannot load module from {module_path}")
                    return False

                module = importlib.util.module_from_spec(spec)
                sys.modules[module] = module
                spec.loader.exec_module(module)
                for rule in NativeRule.__subclasses__():
                    instance = rule()
                    rs.add(instance)
        except FileNotFoundError:
            self.print_error(f"Could not load native rules from {self.native_rule_module_dir}. Directory does not exist.")
            return False

        self.native_rules = rs
        return True
