from dataclasses import dataclass
from sys import stderr

from RuleParser import RuleParser

# TODO might need to allow functions as rules e.g. for current-time-millis.
# Therefore the RuleSet should use a dictionary internally instead of iterating over the ruleset.
# The RuleSet will then also lookup and execute the function Rules.
# Or, extend Rule with subclass and insert the Rule Object which will override isApplicable!

@dataclass
class RuleSet:

    def __init__(self, parser: RuleParser, *ruleStrings: str):
        self.ruleStrings = ruleStrings
        self.rules = []

        for ruleStr in ruleStrings:
            self.rules.append(parser.parse(ruleStr))

    def apply(self, interpreter):
        while(True):
            ds = interpreter.ds
            cs = interpreter.cs
            print(f"{interpreter.ds} | {interpreter.cs} =", file=stderr)
            for rule in self.rules:
                rule.execute(interpreter)

            if interpreter.ds == ds and interpreter.cs == cs:
                print("No more possible rules for application", file=stderr)
                break

    def __repr__(self) -> str:
        return self.ruleStrings
