from sys import stderr
import RuleParser as RuleParser
from RuleSet import RuleSet
from Stack import Stack
from TerminalEscsapeCodes import TerminalEscapeCodes as TEC

class Interpreter:

    def __init__(self,
            ruleset: RuleSet,
            cs: Stack = Stack(),
            ds: Stack = Stack(),
            trunkPrintOfStackToLength=0,
            displayReasoningChain=True):
        self.ds = ds
        self.cs = cs
        self.trunkPrintOfStackToLength=trunkPrintOfStackToLength
        self.ruleset = ruleset
        self.displayReasoningChain = displayReasoningChain

    def run(self, interactive=False):
        while True:
            try:
                # TODO use readline instead of input for history and autocompletion
                user_input = input("Enter something (or 'exit' to quit and '?' for help):\n> ").strip()
            except EOFError:
                break
            if user_input.startswith('exit'):
                break
            elif user_input.startswith('step'):
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
            else:
                self.print_error("This seems to be a wrong comment. Please try again.")

    def make_step(self):
        if self.displayReasoningChain:
            self.log_state()

        for rule in self.ruleset.rules:
            if rule.execute(self):
                return True # some rule matched
        return False

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
        save <path>             Save the current ruleset into the given file.
        load <path>             Replaces the current ruleset with the one in the given file.
        append ruleset <path>   Load the given ruleset into the current one.
        """, file=stderr)

    def show_ruleset(self):
        print(f"{TEC.BLUE}{self.ruleset}{TEC.END}", file=stderr)

    def add_rule(self, ruleDesc: str):
        rule = RuleParser.parse(ruleDesc)
        err = self.ruleset.add(rule)
        if err:
            self.print_error(err.msg)

    def remove_rule(self, ruleDesc: str):
        # TODO
        self.print_error("Unfortunately, this isn't currently implemented.")

    def save_ruleset(self, path: str):
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
            rs = RuleSet.load(path)
        except FileNotFoundError:
            self.print_error(f"File not found: {path}")
        except PermissionError:
            self.print_error(f"Permission denied to read file: {path}")
        except IOError as e:
            self.print_error(f"An error occurred while reading the file: {e}")

        self.ruleset = rs

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
