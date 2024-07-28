import re
from Dictionary import Dictionary
from Rule import Rule

class RuleParser:
    def parse(self, ruleStr: str):
        lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
        m_ds_pat, m_cs_pat = self.__parseLeftRuleSide(lhs)
        i_ds_pat, i_cs_pat = self.__parseRightRuleSide(rhs)
        return Rule(mp=m_ds_pat, ocs= m_cs_pat, ip=i_ds_pat, ncs=i_cs_pat)

    def __parseLeftRuleSide(self, str: str):
        *dspStr, cspStr = re.split(r"\s+\|\s+", str)
        dsp = self.__parsePattern(dspStr[0] if dspStr != [] else "")
        csp = self.__parsePattern(cspStr, isCallstack=True)
        return dsp, csp

    def __parseRightRuleSide(self, str: str):
        dspStr, *cspStr = re.split(r"\s+\|\s+", str)
        dsp = self.__parsePattern(dspStr)
        csp = self.__parsePattern(cspStr[0] if cspStr != [] else "", isCallstack=True)
        return dsp, csp

    def __parsePattern(self, str: str, isCallstack=False):
        tokens = re.split(r"\s+", str)

        addRestMatcher = True
        pattern = []
        popIdx = 0
        while tokens != []:
            token = tokens.pop(popIdx)
            if token == "[":
                pattern.append(self.parseStack(tokens))
            elif token == "{":
                pattern.append(self.parseDict(tokens))
            elif token != "":
                if addRestMatcher:
                    addRestMatcher = not token.startswith('@')
                pattern.append(token)

        if isCallstack:
            pattern.reverse()

        if addRestMatcher:
            pattern = ["@RCS" if isCallstack else "@RDS"] + pattern

        return pattern

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
