
from dataclasses import dataclass
from sys import stderr
from Interpreter import Interpreter
from Rule import IRule
import RuleParser
from RuleSet import RuleSet
from Stack import Stack

@dataclass
class InternalRule(IRule):
    rule_desc: str

    def __repr__(self) -> str:
        return self.rule_desc

class Readline(IRule):
    def execute(self, i: Interpreter):
        if i.cs == [] or i.cs.peek() != "read-line":
            return False

        i.ds.append(input())
        i.cs.pop(0)
        return True

    def __repr__(self) -> str:
        return "readlines"

class Slurp(IRule):
    def execute(self, i: Interpreter):
        if i.cs == [] or i.cs.peek() != "slurp":
            return False

        if i.ds == []:
            return False

        *rest, source = i.ds

        content = ""
        try:
            with open(source, "r") as file:
                content = file.read()
        except FileNotFoundError:
            print("File not found:", source)
        except PermissionError:
            print("Permission denied to read file:", source)
        except IOError as e:
            print("An error occurred while reading the file:", e)

        i.ds = Stack(*rest, content)
        i.cs.pop(0)
        return True

    def __repr__(self) -> str:
        return "slurp"

class Uncomment(IRule):
    def execute(self, i: Interpreter):
        import re

        if i.cs == [] or i.cs.peek() != "uncomment":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        i.ds = Stack(*rest, *[re.sub(r"(?m)\s*%.*$", "", word).strip()])
        i.cs.pop(0)
        return True

    def __repr__(self) -> str:
        return "uncomment"

@dataclass
class Tokenize(InternalRule):
    def __init__(self):
        self.rule_desc = "#TXT_WRD | tokenize -> [ @LINE_WRDS ]"

    def execute(self, i: Interpreter):
        this = RuleParser.parse(self.rule_desc)
        matches = this.matches(i)
        if matches == False:
            return False

        txt = str(matches["#TXT_WRD"])
        lines = Stack(*[part for part in txt.splitlines()])
        data = matches | {"@LINE_WRDS": lines}
        this.instantiate(data, i)
        return True

class AddRuleToRuleset(InternalRule):
    def __init__(self):
        self.rule_desc = "RULE_DESC | add_to_ruleset ->"

    def execute(self, i: Interpreter):
        this = RuleParser.parse(self.rule_desc)
        matches = this.matches(i)
        if matches == False:
            return False

        rule = RuleParser.parse(matches["#RULE_DESC"])
        err = i.ruleset.add(rule)
        if err:
            print(err.msg, file=stderr)

        this.execute(i)
        return True

InitialRules = RuleSet([
    RuleParser.parse("\ #WRD -> #WRD"),
    RuleParser.parse("#PATH | load -> | slurp uncomment tokenize"),
    Readline(),
    Slurp(),
    Uncomment(),
    Tokenize(),
    RuleParser.parse("[ @RULES #RULE_DESC ] | add_to_ruleset -> [ @RULES ] #RULE_DESC | add_to_ruleset add_to_ruleset"),
    # AddRuleToRuleset()
])
