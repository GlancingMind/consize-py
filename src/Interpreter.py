from sys import stderr
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

    def run(self):
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
                print(f"{TEC.RED}No more possible rules for application{TEC.END}", file=stderr)
                # TODO instead of breaking, could ask for further user-input.
                # Use readline for this, which has tab completion.
                # Idee: Could introduce word, which halts current interpretation
                # and goes into this interactive mode, to edit ruleset inplace.
                break

        return self

    def log_state(self):
        """
        Print the current stack states in form of a reasoning-chain.

            \<DS> | \<CS> -->
            \<DS> | \<CS> -->
            ...
        """
        print(f"""{
                self.ds.toString(
                    addEnclosingParenthesis=False,
                    trunkLength=self.trunkPrintOfStackToLength)
                } {TEC.RED}{TEC.BOLD}|{TEC.END} {TEC.BLUE}{
                self.cs.toString(
                    addEnclosingParenthesis=False,
                    trunkLength=self.trunkPrintOfStackToLength)
                }{TEC.END} {TEC.BOLD}{TEC.RED}-->{TEC.END}""", file=stderr)
