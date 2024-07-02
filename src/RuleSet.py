from dataclasses import dataclass

from RuleParser import RuleParser

# TODO RuleSet could construct a dictionary from rules to lookup rules matching
# word instead of iterating over them.
# TODO might need to allow functions as rules e.g. for current-time-millis.
# Therefore the RuleSet should use a dictionary internally instead of iterating over the ruleset.
# The RuleSet will then also lookup and execute the function Rules.
# Or, extend Rule with subclass and insert the Rule Object which will override isApplicable!

@dataclass
class RuleSet:
    def __init__(self, parser: RuleParser, *ruleStrings: str):
        # TODO somehow this lets all test (except the first one) fail...
        # self.rules = map(lambda ruleStr: parser.parse(ruleStr) , ruleStrings)
        self.rules = []
        for ruleStr in ruleStrings:
            self.rules.append(parser.parse(ruleStr))
        self.ruleStrings = ruleStrings

    def apply(self, interpreter):
        rules = tuple(rule for rule in self.rules if rule.isApplicable(interpreter))
        if not any(rules):
            return "No more rules possible for further substitution"

        for rule in rules:
            interpreter.stack = rule.execute(interpreter)
        return interpreter.stack

    def __repr__(self) -> str:
        return self.ruleStrings
