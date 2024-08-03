from Stack import Stack

# Could also be called StackDescription/
class StackPattern:
    def __init__(self, pattern: Stack) -> None:
        self.pattern = pattern

    def isGeneralizationOf(pattern: Stack):
        # TODO convert the pattern
        return False

    def isSatisfiedBy(self, stk: Stack) -> bool:
        return False

    # TODO stack should be of type StackElement
    # Put all these elements into one Module: Stack.
    def matches(self, pattern: Stack, stack: Stack, topOfStackIsLeft=False):
        pattern = pattern.copy()
        # ds can also be a word (string) which doesn't have copy methode.
        stack = stack.copy() if isinstance(stack, Stack) else stack

        if pattern == [] and stack == []:
            return {}
        if pattern == []:
            return "f"
        if type(stack) != type(pattern):
            return "f"

        foundMatches = {}
        tuples = []
        popIdx = 0 if topOfStackIsLeft else -1
        containsAtMatcher = False

        while pattern != []:
            matcher = pattern.pop(popIdx)
            match matcher:
                case str() if matcher.startswith("@"):
                    tuples.append((matcher, stack))
                    popIdx = -1 if topOfStackIsLeft else 0
                    containsAtMatcher = True
                case str() if matcher.startswith("#"):
                    if stack == []:
                        return "f"
                    tuples.append((matcher, stack.pop(popIdx)))
                case str(): # Literal
                    if stack == []:
                        return "f"
                    e = stack.pop(popIdx)
                    if matcher != e:
                        return "f"
                case Stack() | Dictionary():
                    if stack == []:
                        return "f"
                    m = self.matches(matcher, stack.pop(popIdx), topOfStackIsLeft=True)
                    if m == "f":
                        return m
                    for k,v in m.items():
                        if foundMatches.get(k, v) != v:
                            return "f"
                        foundMatches[k] = v

        if stack != [] and not containsAtMatcher:
            return "f"

        for t in tuples:
            k,v = t
            if foundMatches.get(k, v) != v:
                return "f"
            foundMatches[k] = v

        return foundMatches
