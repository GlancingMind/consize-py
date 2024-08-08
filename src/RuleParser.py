from dataclasses import dataclass
import re
from Rule import Rule
from Stack import Stack
import StackParser
import StackPattern
from StackPattern import StackPattern

@dataclass
class ParseError():
    msg: str

def parse(ruleStr: str):
    # TODO maybe use regex pattern matching groups
    # ^(?P<lhs>((?P<dsp>(\w+\s+)*)\|\s+)?(?P<csp>(\w+\s+)*))(?P<operator>->|=>)(?P<rhs>(?P<dst>(\s+\w+)+)\s+\|(?P<cst>(\s+\w+)*))$

    trimmedRuleStr = ruleStr.strip()
    if "->" in trimmedRuleStr:
        lhs, rhs = re.split(r"\s*->\s*", ruleStr, 1)
        autoAppendRestMatcher = True
    elif "=>" in trimmedRuleStr:
        lhs, rhs = re.split(r"\s*=>\s*", ruleStr, 1)
        autoAppendRestMatcher = False
    else:
        return ParseError(f"The rule `{ruleStr}` description is syntacically wrong")


    m_ds_pat, m_cs_pat = _parse_lh_ruleside(lhs, autoAppendRestMatcher)
    i_ds_pat, i_cs_pat = _parse_rh_ruleside(rhs, autoAppendRestMatcher)
    return Rule(dsp=m_ds_pat, csp= m_cs_pat, dst=i_ds_pat, cst=i_cs_pat, rule_desc=trimmedRuleStr)

def _parse_lh_ruleside(sideStr: str, autoAppendRestMatcher=False):
    *dspStr, cspStr = re.split(r"\s*\|\s+", sideStr)
    dsp = StackParser.parse(dspStr[0] if dspStr != [] else "")
    csp = StackParser.parse(cspStr)

    if autoAppendRestMatcher:
        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = Stack("@RDS", *dsp)

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = Stack(*csp, "@RCS")

    return StackPattern(dsp), StackPattern(csp)

def _parse_rh_ruleside(sideStr: str, autoAppendRestMatcher=False):
    dstStr = ""
    cstStr = ""
    matches = re.finditer(r"\s*(?P<dst>(\s*[^\s|]+)*)?(\s+\|(?P<cst>(\s+[^\s|]+)*))?", sideStr)
    for match in matches:
        if match.group("dst"):
            dstStr += match.group("dst")
        if match.group("cst"):
            cstStr += match.group("cst")
    # dspStr, *cspStr = re.split(r"\s+\|\s*", sideStr)
    dsp = StackParser.parse(dstStr)
    csp = StackParser.parse(cstStr)

    if autoAppendRestMatcher:
        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = Stack("@RDS", *dsp)

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = Stack(*csp, "@RCS")

    return StackPattern(dsp), StackPattern(csp)
