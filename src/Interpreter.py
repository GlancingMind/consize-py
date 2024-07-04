from RuleSet import RuleSet

class Interpreter:

    def __init__(self, rules: RuleSet, cs: list = [], ds: list = []):
        self.rules = rules
        self.ds = ds
        self.cs = cs

    def run(self):
        self.rules.apply(self)
