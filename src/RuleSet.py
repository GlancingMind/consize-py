from dataclasses import dataclass
from typing import SupportsIndex

from Rule import Rule
from RuleParser import RuleParser

@dataclass
class Error():
    msg: str

@dataclass
class RuleSet:
    def __init__(self, parser: RuleParser, *ruleStrings: str, rules: list[Rule]=[]):
        self.ruleStrings = ruleStrings
        self.rules: list[Rule] = []

        for ruleStr in ruleStrings:
            self.rules.append(parser.parse(ruleStr))

        self.rules += rules

    def add(self, rule: Rule) -> None|Error:
        return self.add_by_index(rule)

    def add_by_index(self, rule: Rule, idx: SupportsIndex=-1) -> None|Error:
        # TODO check if rule can be added to ruleset => Might be ambiguise
        try:
            self.rules.insert(idx, rule)
        except Exception as e:
            return Error(f"The rule could not be added to the ruleset. Reason: {str(e)}")
        return None

    def remove(self, rule: Rule):
        self.remove(self.rules.index(rule))

    def remove_by_index(self, idx: SupportsIndex):
        self.rules.pop(idx)

    def __repr__(self) -> str:
        return ("\n").join(str(rule) for rule in self.rules)
