from dataclasses import dataclass

from Rule import Rule
from RuleParser import RuleParser

@dataclass
class RuleSet:
    def __init__(self, parser: RuleParser, *ruleStrings: str, rules: list[Rule]=[]):
        self.ruleStrings = ruleStrings
        self.rules: list[Rule] = []

        for ruleStr in ruleStrings:
            self.rules.append(parser.parse(ruleStr))

        self.rules += rules

    def add(self, rule: Rule):
        pass

    def remove(self, rule: Rule):
        pass

    def __repr__(self) -> str:
        return self.ruleStrings
