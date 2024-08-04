from dataclasses import dataclass
from sys import stderr

from Rule import Rule
from RuleParser import RuleParser

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
        # counter = 0
        while(True):
            ds = interpreter.ds
            cs = interpreter.cs
            print(f"{interpreter.ds.toString(addEnclosingParenthesis=False)} | {cs.toString(addEnclosingParenthesis=False, tosIsLeft=True)} ==>", file=stderr)

            # TODO This should be a CLI option
            # counter = counter + 1
            # if counter == 15:
            #     print("Stop due to print length", file=stderr)
            #     break

            # TODO these could be a generator, return a rule that matches, if no
            # rule is returned, exit.
            someRuleMatched = False
            for rule in self.rules:
                someRuleMatched = rule.execute(interpreter)
                if someRuleMatched:
                    break

            if not someRuleMatched:
                print("No more possible rules for application", file=stderr)
                break

    def __repr__(self) -> str:
        return self.ruleStrings
