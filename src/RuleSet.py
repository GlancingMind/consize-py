from dataclasses import dataclass
from typing import SupportsIndex

from Rule import IRule
import RuleParser

@dataclass
class RuleSet:
    rules: list[IRule]

    @staticmethod
    def load(path: str):
        # TODO maybe take an additional callback, which is called for
        # encountered errors.
        content = ""
        with open(path, "r") as file:
            content = file.read()

        # remove all comments
        import re
        content = re.sub(r"(?m)\s*%.*$", "", content)
        lines = content.splitlines()

        rs = RuleSet([])

        for line in lines:
            if line != "":
                err, rule = RuleParser.parse(line)
                if err:
                    return err,None
                rs.add(rule)

        return None,rs

    def add(self, rule: IRule):
        return self.add_by_index(rule, len(self.rules))

    def add_by_index(self, rule: IRule, idx: SupportsIndex):
        # TODO check for ambiguity of rule befor adding to ruleset
        # Or add a validate methode, to validate whole RuleSet by some validator
        self.rules.insert(idx, rule)

    # TODO rename to add
    def append(self, ruleset: 'RuleSet'):
        for rule in ruleset.rules:
            self.add(rule)

    def remove(self, rule: IRule):
        self.remove(self.rules.index(rule))

    def remove_by_index(self, idx: SupportsIndex):
        self.rules.pop(idx)

    def __iter__(self):
        return self.rules.__iter__()

    def __repr__(self) -> str:
        return ("\n").join(str(rule) for rule in self.rules)
