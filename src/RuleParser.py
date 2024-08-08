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
    tokens = re.split(r"\s+", sideStr)
    dsp = []
    csp = []
    if "|" in tokens:
        index = tokens.index("|")
        dsp = tokens[:index]
        csp = tokens[index + 1:]
    else:
        csp = tokens

    dsp, _ = StackParser.parse_stack(dsp)
    csp, _ = StackParser.parse_stack(csp)

    if autoAppendRestMatcher:
        if not any(word.startswith("@") for word in dsp if isinstance(word, str)):
            dsp = Stack("@RDS", *dsp)

        if not any(word.startswith("@") for word in csp if isinstance(word, str)):
            csp = Stack(*csp, "@RCS")

    return StackPattern(dsp), StackPattern(csp)

def _parse_rh_ruleside(sideStr: str, autoAppendRestMatcher=False):
    tokens = re.split(r"\s+", sideStr)
    dst = []
    cst = []
    if "|" in tokens:
        index = tokens.index("|")
        dst = tokens[:index]
        cst = tokens[index + 1:]
    else:
        dst = tokens

    dst, _ = StackParser.parse_stack(dst)
    cst, _ = StackParser.parse_stack(cst)

    if autoAppendRestMatcher:
        if not any(word.startswith("@") for word in dst if isinstance(word, str)):
            dst = Stack("@RDS", *dst)

        if not any(word.startswith("@") for word in cst if isinstance(word, str)):
            cst = Stack(*cst, "@RCS")

    return StackPattern(dst), StackPattern(cst)
