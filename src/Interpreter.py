import importlib
import importlib.util
import os
import subprocess
from sys import stderr
import sys
import tempfile
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
        self.trunkPrintOfStackToLength=trunkPrintOfStackToLength
        self.displayReasoningChain = displayReasoningChain
        self.native_rule_module_dir = native_rule_module_dir
        self.ruleset = ruleset
        self.native_rules = RuleSet([])
        if self.native_rule_module_dir:
            self.discover_native_rules()

    def run(self, interactive=False):
        while True:
            if self.displayReasoningChain:
                self.log_state()
            try:
                if interactive:
                    # TODO use readline instead of input for history and autocompletion
                    user_input = input("Enter something (or 'exit' to quit and '?' for help):\n> ").strip()
                else:
                    # will skip to continue step, which evaluate all rules to the end.
                    user_input = "continue"
            except EOFError:
                break

            if user_input.startswith('exit'):
                break
            elif user_input.startswith('step') or user_input == "":
                if not self.make_step():
                    print(f"{TEC.RED}No applicative rules found{TEC.END}", file=stderr)
            elif user_input.startswith('continue'):
                while self.make_step():
                    pass
                print(f"{TEC.RED}No applicative rules found{TEC.END}", file=stderr)
                if not interactive:
                    break
            elif user_input.startswith('?'):
                self.show_help()
            elif user_input.startswith('status'):
                self.log_state()
            elif user_input.startswith('rules'):
                self.show_ruleset()
            elif user_input.startswith('+'):
                ruleDesc = user_input.removeprefix("+").strip()
                if ruleDesc == "":
                    self.print_error("No rule description given.")
                self.add_rule(ruleDesc)
            elif user_input.startswith('-'):
                ruleDesc = user_input.removeprefix("-").strip()
                if ruleDesc == "":
                    self.print_error("No rule description given.")
                self.remove_rule(ruleDesc)
            elif user_input.startswith('save'):
                path = user_input.removeprefix("save").strip()
                if path == "":
                    self.print_error("No path given.")
                else:
                    self.save_ruleset(path)
            elif user_input.startswith('load'):
                path = user_input.removeprefix("load").strip()
                if path == "":
                    self.print_error("No path given.")
                else:
                    self.replace_ruleset(path)
            elif user_input.startswith('append ruleset'):
                path = user_input.removeprefix("append ruleset").strip()
                if path == "":
                    self.print_error("No path given.")
                else:
                    self.append_ruleset(path)
            elif user_input.startswith('rediscover'):
                self.discover_native_rules()
            else:
                # No interpreter command given, treat input as data to call-/datastack
                self.cs = Stack(*StackParser.parse(user_input), *self.cs)
                self.make_step()

    def make_step(self,):
        some_rule_applied = False
        for rule in self.ruleset.rules:
            if rule.execute(self):
                some_rule_applied = True
                break
        for rule in self.native_rules.rules:
            if rule.execute(self):
                some_rule_applied = True
                break

        if not some_rule_applied:
            # If word wasn't found, move it from the callstack to the datastack
            wrd, *rcs = self.cs
            self.ds.append(wrd)
            self.cs = Stack(*rcs)

        return some_rule_applied

    def discover_native_rules(self):
        # TODO does this also remove modules, which are no longer available?
        rs = RuleSet([])
        try:
            for module_name in os.listdir(self.native_rule_module_dir):
                module_path = os.path.join(self.native_rule_module_dir, module_name)
                if not os.path.isfile(module_path):
                    continue

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is None:
                    self.print_error(f"Cannot load module from {module_path}")

                module = importlib.util.module_from_spec(spec)
                sys.modules[module] = module
                spec.loader.exec_module(module)
                for rule in NativeRule.__subclasses__():
                    rs.add(rule)
        except FileNotFoundError:
            self.print_error(f"Could not load native rules from {self.native_rule_module_dir}. Directory does not exist.")
        self.native_rules = rs

    def print_error(self, msg: str):
        print(f"{TEC.RED}{TEC.BOLD}{msg}{TEC.END}", file=stderr)

    def log_state(self):
        datastack=self.ds.toString(addEnclosingParenthesis=False, trunkLength=self.trunkPrintOfStackToLength)
        callstack=self.cs.toString(addEnclosingParenthesis=False, trunkLength=self.trunkPrintOfStackToLength)
        step =f"{datastack} {TEC.RED}{TEC.BOLD}|{TEC.END} {TEC.BLUE}{callstack}{TEC.END} {TEC.BOLD}{TEC.RED}-->{TEC.END}"
        print(step, file=stderr)

    def show_help(self):
        print(
        """
        Commands:
        ?                       Shows this help.
        exit                    Quits the program.
        step                    Try next execution step.
        continue                Continues rule evaluation.
        status                  Shows current evaluation state.
        rules                   Shows all current rules.
        + <Rule Description>    Add rule to current ruleset.
        - <Rule Description>    Remove rule from current ruleset. (Not yet implemented)
        edit                    Open the current ruleset within an editor and load it on save.
        save <path>             Save the current ruleset into the given file.
        load <path>             Replaces the current ruleset with the one in the given file.
        append ruleset <path>   Load the given ruleset into the current one.
        rediscover              Rediscover native rules.
        """, file=stderr)

    def show_ruleset(self):
        print(f"{TEC.BLUE}{self.ruleset}{TEC.END}", file=stderr)
        print(f"{TEC.BOLD}And following native rules:{TEC.END}")
        print(f"{TEC.BLUE}{self.native_rules}{TEC.END}", file=stderr)

    def add_rule(self, ruleDesc: str):
        rule = RuleParser.parse(ruleDesc)
        err = self.ruleset.add(rule)
        if err:
            self.print_error(err.msg)

    def remove_rule(self, ruleDesc: str):
        # TODO
        self.print_error("Unfortunately, this isn't currently implemented.")

    def save_ruleset(self, path: str):
        # TODO should probably also write the rule native rules as comments into
        # the ruleset. Just for information, that some rules might not be
        # available. Sharing the ruleset-file.
        try:
            with open(path, "w") as file:
                file.write(str(self.ruleset))
        except FileNotFoundError:
            self.print_error(f"File not found: {path}")
        except PermissionError:
            print(f"Permission denied to write file: {path}")
        except IOError as e:
            print(f"An error occurred while writing the file: {e}")

    def replace_ruleset(self, path: str):
        try:
            self.ruleset = RuleSet.load(path)
        except FileNotFoundError:
            self.print_error(f"File not found: {path}")
        except PermissionError:
            self.print_error(f"Permission denied to read file: {path}")
        except IOError as e:
            self.print_error(f"An error occurred while reading the file: {e}")

    def append_ruleset(self, path: str):
        try:
            rs = RuleSet.load(path=path)
        except FileNotFoundError:
            self.print_error(f"File not found: {path}")
        except PermissionError:
            self.print_error(f"Permission denied to read file: {path}")
        except IOError as e:
            self.print_error(f"An error occurred while reading the file: {e}")
        self.ruleset.append(rs)

    def edit_ruleset(self):
        encounteredError = False
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            # Write the current ruleset to the temporary file
            temp_file.write(str(self.ruleset).encode('utf-8'))
            temp_file.close()  # Close the file to ensure it's saved

            # Open the users prefered text-editor, otherwise nano
            editor = os.environ.get('EDITOR', 'nano')  # Default to 'nano' if EDITOR is not set
            try:
                subprocess.run([editor, temp_file.name])
            except Exception as e:
                self.print_error(f"Failed to open the editor. Error: {e}")
                encounteredError = True

            # Read the content of the file after the editor is closed
            if not encounteredError:
                self.replace_ruleset(temp_file.name)

        # Clean up the temporary file
        os.remove(temp_file.name)
