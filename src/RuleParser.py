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
        tokens = re.split(r"\s+", dspStr[0] if dspStr != [] else "")
        dsp = [] if all(t == "" for t in tokens) else self.__parsePattern(tokens)
        tokens = re.split(r"\s+", cspStr)
        csp = [] if all(t == "" for t in tokens) else self.__parsePattern(tokens)

        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = ["@RDS"] + dsp

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = csp + ["@RCS"]
        csp.reverse()

        return dsp, csp

    def __parseRightRuleSide(self, sideStr: str):
        dspStr, *cspStr = re.split(r"\s*\|\s+", sideStr)
        tokens = re.split(r"\s+", dspStr)
        dsp = [] if all(t == "" for t in tokens) else self.__parsePattern(tokens)
        tokens = re.split(r"\s+", cspStr[0] if cspStr != [] else "")
        csp = [] if all(t == "" for t in tokens) else self.__parsePattern(tokens)

        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = ["@RDS"] + dsp

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = csp + ["@RCS"]
        csp.reverse()

        return dsp, csp

    def __parsePattern(self, tokens: list[str]):
        pattern = []
        while tokens != []:
            token = tokens.pop(0)
            if token == "[":
                pattern.append(self.__parsePattern(tokens))
            elif token == "]":
                return pattern
            elif token == "{":
                pattern.append(self.__parseDict(tokens))
            else:
                pattern.append(token)
        return pattern

    def __parseDict(self, tokens: list[str]):
        d = Dictionary()
        while tokens != []:
            token = tokens.pop(0)
            if token == "{":
                d.append(self.__parseDict(tokens))
            elif token == "}":
                break
            else:
                value = self.__parsePattern([token])
                # The result of __parsePattern will be always a stack.
                # Therefore __parsePattern([b]) for { a b }, will return [b].
                # But what we want is the unwrapped b, therefore we unwrap it.
                # What if { a [ b ] } is given?
                # Then __parsePattern will return
                # [[b]], which will be unwrapped, yielding the correct value [b].
                if len(value) == 1:
                    d.append(value[0])
                else:
                    d.append(value)

        return d
