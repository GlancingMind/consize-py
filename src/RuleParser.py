import re
from Rule import Rule

class RuleParser:
    def parse(self, ruleStr: str) -> Rule:
        """
        Parses a rule of following form: #S #F | swap -> #F #S
        """
        lhs, rhs = re.split(r"\s*->\s*", ruleStr)
        lhsRule = self.__parseRuleSide(lhs)
        rhsRule = self.__parseRuleSide(rhs, isLeftSide=False)
        return Rule(*(lhsRule + rhsRule))

    def __parseRuleSide(self, ruleStr, isLeftSide=True):
        """
        Parses a rule of following form: (#DATA #PATTERN |)? CALLSTACK
        """
        tokens = re.split(r"\s+", ruleStr)
        cs = []
        ds = []
        # Find the index of the '|' symbol, if it exists
        leftOfPipe, *rightOfPipe = re.split("\s*\|\s*", ruleStr, 1)

        if rightOfPipe == [] and isLeftSide:
            cs = "".join(leftOfPipe).split(" ")
            ds = "".join(rightOfPipe).split(" ")
        else:
            ds = "".join(leftOfPipe).split(" ")
            cs = "".join(rightOfPipe).split(" ")

        if ds == [""]:
            ds = []
        if cs == [""]:
            cs = []

        # Convert the ds_tokens into a nested list structure if ds_tokens is not empty
        # ds = parse_list_from_tokens(ds_tokens) if ds_tokens else []

        return self.__parse_list_from_tokens(ds) + ["@RDS"], self.__parse_list_from_tokens(cs) + ["@RCS"]
        # NOTE @RDS is appended to both patterns to match the remaining DS otherwise
        # match will result in false. Reason:
        #   [ 1 2 ] isn't matched by the sole pattern [ 1 ].
        # By appending @RDS 2 will be matched by @RDS.
        # NOTE @RDS can be always appended, as it will be the last element in the
        # rule. If the user specifies @RDS himself, his @RDS will be filled first
        # and the appended @RDS wont match anything. This also holds true, when the
        # users uses a different name for the tail-matcher.

    def __parse_list_from_tokens(self, tokens):
        stack = []
        current = []
        for token in tokens:
            if token == '[':
                stack.append(current)
                current = []
            elif token == ']':
                if stack:
                    temp = current
                    current = stack.pop()
                    current.append(temp)
            else:
                current.append(token)
        return current
