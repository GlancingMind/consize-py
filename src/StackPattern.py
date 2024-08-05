from dataclasses import dataclass

from Stack import Dictionary, Stack, StackElement

@dataclass
class StackPattern():
    def __init__(self, stk = Stack):
        self.pattern = stk

    def __repr__(self) -> str:
        return str(self.pattern)

    def copy(self):
        return self.pattern.copy()

    def __iter__(self):
        return iter(self.pattern)


def match(pattern: StackPattern, stack: StackElement, topOfStackIsLeft=False):
    pattern = pattern.copy()
    # ds can also be a word (string) which doesn't have copy methode.
    # Can remove the if, when 'Word' is used instead of str.
    stack = stack.copy() if isinstance(stack, Stack) or isinstance(stack, Dictionary) else stack

    if pattern == [] and stack == []:
        return {}
    if pattern == []:
        return False
    if type(stack) != type(pattern):
        return False

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
                    return False
                tuples.append((matcher, stack.pop(popIdx)))
            case str(): # Literal
                if stack == []:
                    return False
                e = stack.pop(popIdx)
                if matcher != e:
                    return False
            case Stack() | Dictionary():
                if stack == []:
                    return False
                m = match(matcher, stack.pop(popIdx), topOfStackIsLeft=True)
                if m == False:
                    return m
                for k,v in m.items():
                    if foundMatches.get(k, v) != v:
                        return False
                    foundMatches[k] = v

    if stack != [] and not containsAtMatcher:
        return False

    for t in tuples:
        k,v = t
        if foundMatches.get(k, v) != v:
            return False
        foundMatches[k] = v

    return foundMatches

def instantiate(pattern: StackPattern, data: dict|bool):
    stk = Stack()

    # When match doesn't match, 'f' is returned.
    # But instantiate requires a dictionary as data,
    # therefore we will propagate the error upwards.
    # This also has the adventage, that the equal?-rule:
    # Will implicitly return 'f' when the compared values wont match.
    if not data:
        return 'f'

    for matcher in pattern:
        match matcher:
            case Dictionary():
                d = instantiate(matcher, data)
                if d == []:
                    stk += [Dictionary()]
                else:
                    stk += [Dictionary(*d)]
            case Stack():
                stk += [instantiate(matcher, data)]
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
