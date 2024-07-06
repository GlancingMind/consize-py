from dataclasses import dataclass
from sys import stderr

from PrefixTrie import PrefixTrie
from RuleParser import RuleParser

# TODO might need to allow functions as rules e.g. for current-time-millis.
# Therefore the RuleSet should use a dictionary internally instead of iterating over the ruleset.
# The RuleSet will then also lookup and execute the function Rules.
# Or, extend Rule with subclass and insert the Rule Object which will override isApplicable!

@dataclass
class RuleSet:

    def __list2DecisionTree(self, l):
        h, *t = l
        if t:
            return {h: self.__list2DecisionTree(t)}
        return h

    def __init__(self, parser: RuleParser, *ruleStrings: str):
        self.ruleStrings = ruleStrings
        self.rules = PrefixTrie()

        for ruleStr in ruleStrings:
            rule = parser.parse(ruleStr)
            # TODO dont put in the whole rule as value, instead place the rhs of the rule as new rule into the ruleset.
            # NOTE that the rhs can also contain patterns, which need to be evaluated after retrieval by search.
            self.rules.insert(rule.cs[1:], rule)
            self.rules.insert(rule.ncs[1:], rule)

    def apply(self, interpreter):
        while(True):
            # TODO ds isn't used, as rules are looked up by cs only, ATM.
            ds = interpreter.ds
            cs = interpreter.cs
            for rule in self.rules.search(reversed(cs)):
                print(f"{interpreter.ds} | {interpreter.cs} =", sep=" ", file=stderr)
                rule.execute(interpreter)

            if interpreter.ds == ds and interpreter.cs == cs:
                print("No more possible rules for application", file=stderr)
                break

    def __repr__(self) -> str:
        return self.ruleStrings
