import re
from dataclasses import dataclass
from collections import ChainMap

def parseLeftRuleSide(ruleStr):
    """
    Parses a rule of following form: (#DATA #PATTERN |)? CALLSTACK
    """
    tokenz = re.split(r"\s", ruleStr)
    cs = []
    ds = []
    for token in tokenz:
        if token == "|":
            ds = cs
            cs = []
            continue
        cs += [token]
    return cs + ["@RCS"], ds + ["@RDS"]
    # NOTE @RDS is appended to both patterns to match the remaining DS otherwise
    # match will result in false. Reason:
    #   [ 1 2 ] isn't matched by the sole pattern [ 1 ].
    # By appending @RDS 2 will be matched by @RDS.
    # NOTE @RDS can be always appended, as it will be the last element in the
    # rule. If the user specifies @RDS himself, his @RDS will be filled first
    # and the appended @RDS wont match anything. This also holds true, when the
    # users uses a different name for the tail-matcher.

def parseRightRuleSide(ruleStr):
    """
    Parses a rule of following form: #DATA #PATTERN (| CALLSTACK)?
    """
    tokenz = re.split(r"\s", ruleStr)
    cs = []
    ds = []
    for token in tokenz:
        if token == "|":
            cs = ds
            ds = []
            continue
        if token != '':
            ds += [token]
    return cs + ["@RCS"], ds + ["@RDS"]

def parseRuleString(ruleStr):
    """
    Parses a rule of following form: #S #F | swap -> #F #S
    """
    lhs, rhs = re.split(r"\s*->\s*", ruleStr)
    lhsRule = parseLeftRuleSide(lhs)
    rhsRule = parseRightRuleSide(rhs)
    return lhsRule + rhsRule

@dataclass
class Rule:
    def __repr__(self) -> str:
        return self.ruleStr

    def __init__(self, ruleStr):
        self.ruleStr = ruleStr
        self.cs, self.mp, self.ncs, self.ip = parseRuleString(ruleStr)

    def isApplicable(self, interpreter):
        return interpreter.cs != [] and interpreter.cs[0] == self.cs[0] and match(self.mp, interpreter.ds) != ['f']

    def execute(self, interpreter):
        return rewrite(self.mp, self.ip)(interpreter.ds)

def match(pattern, ds):
    if pattern == [] and ds == []:
        return [{}]
    if pattern == []:
        return ["f"]

    m = []
    matcher, *rstPat = pattern
    match matcher:
        case list():
            word, *rstData = ds
            m += match([rstPat, rstData]) + match([matcher, word])
            if "f" in m:
                return ["f"]
            return [dict(ChainMap(*m))]
        case str() if matcher.startswith('@'):
            return [{ matcher: ds }]
        case str():
            if ds == []:
                return ["f"]
            word, *rstData = ds
            if matcher.startswith('#'):
                m +=  match(rstPat, rstData) + [{matcher: word}]
            elif word != matcher:
                return ["f"]
            elif word == matcher:
                m += match(rstPat, rstData) + [{}]

    if "f" in m:
        return ["f"]
    if matcher in m[0].keys() and m[0][matcher] != word:
        return ["f"]
    return [dict(ChainMap(*m))]

def instantiate(pattern, data):
    stk = []

    # When match doesn't match, 'f' is returned.
    # But instantiate requires a dictionary as data,
    # therefore we will propagate the error upwards.
    # This also has the adventage, that the equal?-rule:
    # Will implicitly return 'f' when the compared values wont match.
    if data == 'f':
        return data

    for matcher in pattern:
        if matcher.startswith('@'):
            stk += data[matcher]
        elif matcher.startswith('#'):
            stk += [data[matcher]]
        else:
            stk += [matcher]
    return stk

def rewrite(mpat, ipat):
    return lambda data: instantiate(ipat, match(mpat, data)[0])
