import re
from Rule import Rule

class RuleParser:
    def parse(self, ruleStr: str) -> Rule:
        """
        Parses a rule of following form: #S #F | swap -> #F #S
        """
        lhs, rhs = re.split(r"\s*->\s*", ruleStr)
        lhsRule = self.__parseLeftRuleSide(lhs)
        rhsRule = self.__parseRightRuleSide(rhs)
        return Rule(*(lhsRule + rhsRule))

    def __parseLeftRuleSide(self, ruleStr):
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

    def __parseRightRuleSide(self, ruleStr):
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
