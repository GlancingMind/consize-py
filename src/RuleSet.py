from dataclasses import dataclass
from sys import stderr

from Rule import Rule
from RuleParser import RuleParser
from StackSerializer import stringify_stack

# TODO might need to allow functions as rules e.g. for current-time-millis.
# Therefore the RuleSet should use a dictionary internally instead of iterating over the ruleset.
# The RuleSet will then also lookup and execute the function Rules.
# Or, extend Rule with subclass and insert the Rule Object which will override isApplicable!

@dataclass
class RuleSet:

    def __init__(self, parser: RuleParser, *ruleStrings: str, rules: list[Rule]=[]):
        self.ruleStrings = ruleStrings
        self.rules = []

        for ruleStr in ruleStrings:
            self.rules.append(parser.parse(ruleStr))

        self.rules += rules

    def apply(self, interpreter):
        print('\n\nSteps:',file=stderr)
        counter = 0
        while(True):
            ds = interpreter.ds
            cs = interpreter.cs
            dsRepr = stringify_stack(interpreter.ds)
            reversedCallstack = interpreter.cs.copy()
            reversedCallstack.reverse()
            csRepr = stringify_stack(reversedCallstack)
            print(f"{dsRepr} | {csRepr} ==>", file=stderr)
            counter = counter + 1
            if counter == 15:
                print("Stop due to print length", file=stderr)
                break

            for rule in self.rules:
                if rule.execute(interpreter):
                    break # doing this to reduce double printing of log entries
                          # and enforces, that rules are matched from the start of the
                          # RuleSet.

            if interpreter.ds == ds and interpreter.cs == cs:
                print("No more possible rules for application", file=stderr)
                break

    def __repr__(self) -> str:
        return self.ruleStrings
