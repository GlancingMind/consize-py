import re
from Dictionary import Dictionary
from Rule import Rule

class RuleParser:
    def parse(self, ruleStr: str):
        lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
        ls = self.__parseLeftRuleSide(lhs)
        rs = self.__parseRightRuleSide(rhs)
        # print(f"{ls} -> {rs}")
        return Rule(*(ls+rs))

    # Can parse a ruleside easiely by treating the whole words as a stack.
    # At least the left side can be popped from continuesly until | is found, then
    # the words are the callstack and everything after it is the datastack.
    # The right side can be processed equally by treating the top of stack on the
    # other side.
    def __parseLeftRuleSide(self, str: str):
        if str == "":
            return []

        tokens = re.split(r"\s+", str)

        appendRDS = True
        cs = []
        ds = []
        curStack = []
        while tokens != []:
            token = tokens.pop(0)
            if token == "|":
                ds = curStack
                curStack = []
            elif token == "[":
                curStack.append(self.parseStack(tokens))
            elif token == "{":
                curStack.append(self.parseDict(tokens))
            elif token != "":
                if appendRDS:
                    appendRDS = not token.startswith('@')
                curStack.append(token)

        if cs == []:
            cs = curStack
        else:
            ds = curStack

        if appendRDS:
            ds = ["@RDS"] + ds

        cs = ["@RCS"] + cs
        # cs.append("@RCS")

        return ds, cs

    def __parseRightRuleSide(self, str: str):
        tokens = re.split(r"\s+", str)

        appendRCS = True
        cs = []
        ds = []
        curStack = []
        while tokens != []:
            token = tokens.pop(0)
            if token == "|":
                ds = curStack
                curStack = []
            elif token == "[":
                curStack.append(self.parseStack(tokens))
            elif token == "{":
                curStack.append(self.parseDict(tokens))
            elif token != "":
                if appendRCS:
                    appendRCS = not token.startswith('@')
                curStack.append(token)

        if ds == []:
            ds = curStack
        else:
            cs = curStack

        # TODO for the rhs, the RCS might be always present
        if appendRCS:
            cs.append("@RCS")

        ds = ["@RDS"] + ds

        cs.reverse()
        return ds, cs

    def parseStack(self, tokens: list):
        stack = []
        while tokens != []:
            token = tokens.pop(0)
            if token == "]":
                return stack
            elif token == "[":
                stack.append(self.parseStack(tokens))
            else:
                stack.append(token)

        return stack

    def parseDict(self, tokens: list):
        stack = Dictionary()
        while tokens != []:
            token = tokens.pop(0)
            if token == "{":
                stack.append(self.parseDict(tokens))
            if token == "}":
                break
            else:
                stack.append(token)

        return stack
