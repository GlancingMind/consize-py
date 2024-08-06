from sys import stderr
from RuleParser import RuleParser
from RuleSet import RuleSet
from Stack import Stack
from TerminalEscsapeCodes import TerminalEscapeCodes as TEC

class Interpreter:

    def __init__(self, ruleset: RuleSet, cs: Stack = Stack(), ds: Stack = Stack(), maxRecursionDepth=20, trunkPrintOfStackToLength=0):
        self.ds = ds
        self.cs = cs
        self.maxRecursionDepth=maxRecursionDepth
        self.trunkPrintOfStackToLength=trunkPrintOfStackToLength
        self.ruleset = ruleset

    def run(self, interactive=False):
        print('\n\nSteps:',file=stderr)
        counter = 0
        while(True):
            self.log_state()
            counter = counter + 1
            if counter == self.maxRecursionDepth:
                print("Stop due to print length", file=stderr)
                break

            # TODO these could be a generator, return a rule that matches, if no
            # rule is returned, exit.
            someRuleMatched = False
            for rule in self.ruleset.rules:
                someRuleMatched = rule.execute(self)
                if someRuleMatched:
                    break

            if not someRuleMatched:
                print(f"{TEC.RED}No applicative rules found{TEC.END}", file=stderr)
                if not interactive:
                    break
                else:
                    stopExecution = self.__meta_loop()
                    if stopExecution:
                        break
        return self

    def __meta_loop(self):
        stopExecution = False
        while not stopExecution:
            try:
                # TODO use readline instead of input for history and autocompletion
                user_input = input("Enter something (or 'exit' to quit and '?' for help):\n> ").strip()
            except EOFError:
                stopExecution=True
                break

            # TODO could parse user_input as stack and use StackPattern to match.
            # Or implement this functions completely via ExternalWords-Modules.
            # Should be possible as everyone gets an interpreter reference.
            if user_input.startswith('exit'):
                stopExecution = True
                break
            elif user_input.startswith('continue'):
                break
            if user_input.startswith('?'):
                self.show_help()
            elif user_input.startswith('status'):
                self.log_state()
            elif user_input.startswith('rules'):
                self.show_ruleset()
            elif user_input.startswith('+'):
                ruleDesc = user_input.removeprefix("+").strip()
                if ruleDesc == "":
                    print("No rule description given.", file=stderr)
                self.add_rule(ruleDesc)
            elif user_input.startswith('-'):
                ruleDesc = user_input.removeprefix("-").strip()
                if ruleDesc == "":
                    print("No rule description given.", file=stderr)
                self.remove_rule(ruleDesc)
            elif user_input.startswith('try'):
                ruleDesc = user_input.removeprefix("try").strip()
                if ruleDesc == "":
                    print("No rule description given.", file=stderr)
                self.remove_rule(ruleDesc)
            elif user_input.startswith('save'):
                path = user_input.removeprefix("save").strip()
                if path == "":
                    print("No path given.", file=stderr)
                else:
                    self.save_ruleset(path)
            elif user_input.startswith('load'):
                path = user_input.removeprefix("load").strip()
                if path == "":
                    print("No path given.", file=stderr)
                else:
                    self.save_ruleset(path)
            else:
                print("Sorry, I dont understand.")
        return stopExecution

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
        continue                Continues rule evaluation.
        status                  Shows current evaluation state.
        rules                   Shows all current rules.
        + <Rule Description>    Add rule to current ruleset.
        - <Rule Description>    Remove rule from current ruleset.
        try <Rule Description>  Calls the given rule, but won't add it to the ruleset.
        save <path>             Save the current ruleset into the given file.
        load <path>             Replaces the current ruleset with the one in the given file.
        """, file=stderr)

    def eval(self):
        print("Unfortunately, this isn't currently implemented.")
        pass

    def show_ruleset(self):
        print(str(self.ruleset), file=stderr)

    def add_rule(self, ruleDesc: str) -> bool:
        parser = RuleParser()
        rule = parser.parse(ruleDesc)
        err = self.ruleset.add(rule)
        if err:
            print(err.msg, file=stderr)

    def remove_rule(self, ruleDesc: str):
        # TODO
        print("Unfortunately, this isn't currently implemented.")

    def save_ruleset(self, path: str):
        # TODO
        print("Unfortunately, this isn't currently implemented.")

    def replace_ruleset(self, path: str):
        # TODO
        print("Unfortunately, this isn't currently implemented.")
