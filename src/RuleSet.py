from dataclasses import dataclass

from rule import Rule

# TODO RuleSet could construct a dictionary from rules to lookup rules matching
# word instead of iterating over them.

@dataclass
class RuleSet:
    def __init__(self, *ruleStrings):
        self.rules = map(lambda ruleStr: Rule(ruleStr), ruleStrings)

    def apply(self, interpreter):
        rules = tuple(rule for rule in self.rules if rule.isApplicable(interpreter))
        if not any(rules):
            return "No more rules possible for further substitution"

        for rule in rules:
            interpreter.ds = rule.execute(interpreter)
        return interpreter.ds
