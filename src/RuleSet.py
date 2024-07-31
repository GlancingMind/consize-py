from dataclasses import dataclass
from sys import stderr

from RuleParser import RuleParser
from Dictionary import Dictionary

# TODO might need to allow functions as rules e.g. for current-time-millis.
# Therefore the RuleSet should use a dictionary internally instead of iterating over the ruleset.
# The RuleSet will then also lookup and execute the function Rules.
# Or, extend Rule with subclass and insert the Rule Object which will override isApplicable!

@dataclass
class RuleSet:

    def __init__(self, parser: RuleParser, *ruleStrings: str):
        self.ruleStrings = ruleStrings
        self.rules = []

        for ruleStr in ruleStrings:
            self.rules.append(parser.parse(ruleStr))

    def apply(self, interpreter):
        print('\n\nSteps:',file=stderr)
        while(True):
            ds = interpreter.ds
            cs = interpreter.cs
            dsRepr = self.stringify_stack(interpreter.ds)
            reversedCallstack = interpreter.cs.copy()
            reversedCallstack.reverse()
            csRepr = self.stringify_stack(reversedCallstack)
            print(f"{dsRepr} | {csRepr} ==>", file=stderr)
            for rule in self.rules:
                if rule.execute(interpreter):
                    break # doing this to reduce double printing of log entries
                          # and enforces, that rules are matched from the start of the
                          # RuleSet.

            if interpreter.ds == ds and interpreter.cs == cs:
                print("No more possible rules for application", file=stderr)
                break

    def __repr__(self) -> str:
        return self.ruleStrings

    def stringify_stack(self, lst, printStackParanthesis=False):
        if lst == []:
            return "[ ]"
        s = ' '.join(self.stringify_stack(item, True) if isinstance(item, list) else str(item) for item in lst)
        if printStackParanthesis == True:
            if isinstance(lst, Dictionary):
                s = "{ "+s+" }"
            else:
                s = "[ "+s+" ]"
        return s
