import re
from Rule import Rule
from StackDeserializer import parse, parse_stack

class RuleParser:
    def parse(self, ruleStr: str):
        lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
        m_ds_pat, m_cs_pat = self._parse_lh_ruleside(lhs)
        i_ds_pat, i_cs_pat = self._parse_rh_ruleside(rhs)
        return Rule(mp=m_ds_pat, ocs= m_cs_pat, ip=i_ds_pat, ncs=i_cs_pat)

    def _parse_lh_ruleside(self, sideStr: str):
        *dspStr, cspStr = re.split(r"\s*\|\s+", sideStr)
        tokens = re.split(r"\s+", dspStr[0] if dspStr != [] else "")
        dsp = [] if all(t == "" for t in tokens) else parse(tokens)
        tokens = re.split(r"\s+", cspStr)
        csp = [] if all(t == "" for t in tokens) else parse(tokens)

        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = ["@RDS"] + dsp

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = csp + ["@RCS"]
        csp.reverse()

        return dsp, csp

    def _parse_rh_ruleside(self, sideStr: str):
        dspStr, *cspStr = re.split(r"\s*\|\s+", sideStr)
        tokens = re.split(r"\s+", dspStr)
        dsp = [] if all(t == "" for t in tokens) else parse(tokens)
        tokens = re.split(r"\s+", cspStr[0] if cspStr != [] else "")
        csp = [] if all(t == "" for t in tokens) else parse(tokens)

        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = ["@RDS"] + dsp

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = csp + ["@RCS"]
        csp.reverse()

        return dsp, csp
