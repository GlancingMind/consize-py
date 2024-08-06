import re
from Rule import Rule
from Stack import Stack
from StackPattern import StackPattern
from StackParser import parse

class RuleParser:
    def parse(self, ruleStr: str):
        # TODO use regex pattern matching groups
        # TODO convert to Module. We will never need multiple instances.

        trimmedRuleStr = ruleStr.strip()
        if "->" in trimmedRuleStr:
            lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
            autoAppendRestMatcher = True
        elif "=>" in trimmedRuleStr:
            lhs, rhs = re.split(r"\s*=>\s*", ruleStr, 1)
            autoAppendRestMatcher = False

        m_ds_pat, m_cs_pat = self._parse_lh_ruleside(lhs, autoAppendRestMatcher)
        i_ds_pat, i_cs_pat = self._parse_rh_ruleside(rhs, autoAppendRestMatcher)
        return Rule(dsp=m_ds_pat, csp= m_cs_pat, dst=i_ds_pat, cst=i_cs_pat, rule_desc=trimmedRuleStr)

    def _parse_lh_ruleside(self, sideStr: str, autoAppendRestMatcher=False):
        *dspStr, cspStr = re.split(r"\s*\|\s+", sideStr)
        dsp = parse(dspStr[0] if dspStr != [] else "")
        csp = parse(cspStr)

        if autoAppendRestMatcher:
            if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
                dsp = Stack("@RDS", *dsp)

            if not any(word.startswith("@") for word in csp if isinstance(word, str)):
                csp = Stack(*csp, "@RCS")

        return StackPattern(dsp), StackPattern(csp)

    def _parse_rh_ruleside(self, sideStr: str, autoAppendRestMatcher=False):
        dspStr, *cspStr = re.split(r"\s*\|\s+", sideStr)
        dsp = parse(dspStr)
        csp = parse(cspStr[0] if cspStr != [] else "")

        if autoAppendRestMatcher:
            if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
                dsp = Stack("@RDS", *dsp)

            if not any(word.startswith("@") for word in csp if isinstance(word, str)):
                csp = Stack(*csp, "@RCS")

        return StackPattern(dsp), StackPattern(csp)
