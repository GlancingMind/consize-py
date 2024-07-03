from RuleSet import RuleSet

class Interpreter:

    def __init__(self, rules: RuleSet, stack: list):
        self.stack = stack
        self.rules = rules

    def run(self):
        self.stack = self.rules.apply(self)
        return self.stack

    def printState(self):
        print(self.stack)
