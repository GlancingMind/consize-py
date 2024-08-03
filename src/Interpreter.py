from RuleSet import RuleSet
from Stack import Stack

class Interpreter:

    def __init__(self, rules: RuleSet, cs: Stack = [], ds: Stack = []):
        self.rules = rules
        self.ds = ds
        self.cs = cs

    def run(self):
        self.rules.apply(self)
