import re
from Dictionary import Dictionary
from Rule import Rule

class RuleParser:
    def parse(self, ruleStr: str):
        lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
        m_ds_pat, m_cs_pat = self.__parseLeftRuleSide(lhs)
        i_ds_pat, i_cs_pat = self.__parseRightRuleSide(rhs)
        return Rule(mp=m_ds_pat, ocs= m_cs_pat, ip=i_ds_pat, ncs=i_cs_pat)

    def __parseLeftRuleSide(self, sideStr: str):
        *dspStr, cspStr = re.split(r"\s*\|\s+", sideStr)
        dsp = self.__parsePattern(re.split(r"\s+", dspStr[0] if dspStr != [] else ""))
        csp = self.__parsePattern(re.split(r"\s+", cspStr))

        if all(word == "" for word in dsp if isinstance(word, str)):
            dsp = []

        if all(word == "" for word in csp if isinstance(word, str)):
            csp = []

        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = ["@RDS"] + dsp

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = ["@RCS"] + csp
        csp.reverse()

        return dsp, csp

    def __parseRightRuleSide(self, sideStr: str):
        dspStr, *cspStr = re.split(r"\s*\|\s+", sideStr)
        dsp = self.__parsePattern(re.split(r"\s+", dspStr))
        csp = self.__parsePattern(re.split(r"\s+", cspStr[0] if cspStr != [] else ""))

        if all(word == "" for word in dsp if isinstance(word, str)):
            dsp = []

        if all(word == "" for word in csp if isinstance(word, str)):
            csp = []

        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = ["@RDS"] + dsp

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = ["@RCS"] + csp
        csp.reverse()

        return dsp, csp

    def __parsePattern(self, tokens: list[str]):
        pattern = []
        while tokens != []:
            token = tokens.pop(0)
            if token == "[":
                pattern.append(self.__parsePattern(tokens))
            if token == "]":
                return pattern
            if token == "{":
                pattern.append(self.__parseDict(tokens))
            else:
                pattern.append(token)
        return pattern

    def __parseDict(self, tokens: list[str]):
        d = dict()
        key = None
        while tokens != []:
            token = tokens.pop(0)
            if token == "{":
                d.append(self.__parseDict(tokens))
            if token == "}":
                break
            elif key == None:
                key = token
            else:
                value = self.__parsePattern([token])
                # The result of __parsePattern will be always a stack.
                # Therefore __parsePattern([b]) for { a b }, will return [b].
                # But what we want is the unwrapped b, therefore we unwrap it.
                # What if { a [ b ] } is given?
                # Then __parsePattern will return
                # [[b]], which will be unwrapped, yielding the correct value [b].
                if len(value) == 1:
                    d[key] = value[0]
                else:
                    d[key] = value

        return d
