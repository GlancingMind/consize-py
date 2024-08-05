import re
from Rule import Rule
from Stack import Stack
from StackDeserializer import parse

class RuleParser:
    def parse(self, ruleStr: str):
        # TODO Via the current parsing implementation, the
        #  -> and => cannot be a word within one of the stack patterns.
        # Maybe parsing can be adjusted to allow these arrows within a stack
        # pattern.
        trimmedRuleStr = ruleStr.strip()
        if "->" in trimmedRuleStr:
            lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
            autoAppendRestMatcher = True
        elif "=>" in trimmedRuleStr:
            lhs, rhs = re.split(r"\s*=>\s*", ruleStr, 1)
            autoAppendRestMatcher = False

        m_ds_pat, m_cs_pat = self._parse_lh_ruleside(lhs, autoAppendRestMatcher)
        i_ds_pat, i_cs_pat = self._parse_rh_ruleside(rhs, autoAppendRestMatcher)
        return Rule(mp=m_ds_pat, ocs= m_cs_pat, ip=i_ds_pat, ncs=i_cs_pat)

    def _parse_lh_ruleside(self, sideStr: str, autoAppendRestMatcher=False):
        *dspStr, cspStr = re.split(r"\s*\|\s+", sideStr)
        tokens = re.split(r"\s+", dspStr[0] if dspStr != [] else "")
        dsp = Stack() if all(t == "" for t in tokens) else parse(tokens)
        tokens = re.split(r"\s+", cspStr)
        csp = Stack() if all(t == "" for t in tokens) else parse(tokens)

        if autoAppendRestMatcher:
            if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
                dsp = Stack("@RDS", *dsp)

            if not any(word.startswith("@") for word in csp if isinstance(word, str)):
                csp = Stack(*csp, "@RCS")

        return Stack(*dsp), Stack(*csp)

    def _parse_rh_ruleside(self, sideStr: str, autoAppendRestMatcher=False):
        dspStr, *cspStr = re.split(r"\s*\|\s+", sideStr)
        tokens = re.split(r"\s+", dspStr)
        dsp = Stack() if all(t == "" for t in tokens) else parse(tokens)
        tokens = re.split(r"\s+", cspStr[0] if cspStr != [] else "")
        csp = Stack() if all(t == "" for t in tokens) else parse(tokens)

        if autoAppendRestMatcher:
            if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
                dsp = Stack("@RDS", *dsp)

            if not any(word.startswith("@") for word in csp if isinstance(word, str)):
                csp = Stack(*csp, "@RCS")

        return Stack(*dsp), Stack(*csp)
