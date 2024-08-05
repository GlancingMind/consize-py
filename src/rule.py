from dataclasses import dataclass

from Stack import Dictionary, Stack, StackElement

@dataclass
class Rule:
    def __repr__(self) -> str:
        return f"{self.mp} | {self.cs} -> {self.nds} | {self.ncs}"

    def __init__(self, mp: Stack, ocs: Stack, ip: Stack, ncs: Stack):
        self.mp = mp
        self.cs = ocs
        self.nds = ip
        self.ncs = ncs

    def execute(self, interpreter):
        csm = self.__match(self.cs, interpreter.cs, topOfStackIsLeft=True)
        dsm = self.__match(self.mp, interpreter.ds)
        if csm == "f" or dsm == "f":
            return False
        matches = csm | dsm
        interpreter.cs = self.__instantiate(self.ncs, matches)
        interpreter.ds = self.__instantiate(self.nds, matches)
        return True

    def __match(self, pattern: Stack, stack: StackElement, topOfStackIsLeft=False):
        pattern = pattern.copy()
        # ds can also be a word (string) which doesn't have copy methode.
        # Can remove the if, when 'Word' is used instead of str.
        stack = stack.copy() if isinstance(stack, Stack) or isinstance(stack, Dictionary) else stack

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
                    m = self.__match(matcher, stack.pop(popIdx), topOfStackIsLeft=True)
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

    def __instantiate(self, pattern, data):
        stk = Stack()

        # When match doesn't match, 'f' is returned.
        # But instantiate requires a dictionary as data,
        # therefore we will propagate the error upwards.
        # This also has the adventage, that the equal?-rule:
        # Will implicitly return 'f' when the compared values wont match.
        if data == 'f':
            return data

        for matcher in pattern:
            match matcher:
                case Dictionary():
                    d = self.__instantiate(matcher, data)
                    if d == []:
                        stk += [Dictionary()]
                    else:
                        stk += [Dictionary(*d)]
                case Stack():
                    stk += [self.__instantiate(matcher, data)]
                case str() if matcher.startswith('@'):
                    stk += data[matcher]
                case str() if matcher.startswith('#'):
                    stk += [data[matcher]]
                case dict():
                    for k in matcher.keys():
                        stk += [data[k]]
                case _:
                    stk += [matcher]
        return stk
