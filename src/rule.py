from dataclasses import dataclass
from collections import ChainMap

@dataclass
class Rule:
    def __repr__(self) -> str:
        return f"{self.mp} | {self.cs} -> {self.ip} | {self.ncs}"

    def __init__(self, mp, ocs, ip, ncs):
        self.mp = mp
        self.cs = ocs
        self.ip = ip
        self.ncs = ncs

    def isApplicable(self, interpreter):
        if interpreter.stack != [] and interpreter.stack[0] == self.cs[0]:
            # TODO can this be done differently, so that the duplicate code in
            # execute also cleans up?
            cs, *r = interpreter.stack
            return self.__match(self.mp, r) != ['f']
        return False

    def execute(self, interpreter):
        cs, *r = interpreter.stack
        return self.__rewrite(self.mp, self.ip)(r)

    def __rewrite(self, mpat, ipat):
        return lambda data: self.__instantiate(ipat, self.__match(mpat, data)[0])

    def __match(self, pattern, ds):
        pattern = pattern.copy()
        # ds can also be a word (string) which doesn't have copy methode.
        ds = ds.copy() if isinstance(ds, list) else ds

        if pattern == [] and ds == []:
            return [{}]
        if pattern == []:
            return ["f"]
        if type(ds) != type(pattern):
            return ["f"]

        foundMatches = {}
        tuples = []
        popIdx = 0
        containsAtMatcher = False

        while pattern != []:
            matcher = pattern.pop(popIdx)
            match matcher:
                case str() if matcher.startswith("@"):
                    tuples.append((matcher, ds))
                    popIdx = -1
                    containsAtMatcher = True
                case str() if matcher.startswith("#"):
                    if ds == []:
                        return ["f"]
                    tuples.append((matcher, ds.pop(popIdx)))
                case str(): # Literal
                    e = ds.pop(popIdx)
                    if matcher != e:
                        return ["f"]
                case dict():
                    e = ds.pop(popIdx)
                    if matcher != e:
                        return ["f"]
                case list():
                    m = self.__match(matcher, ds.pop(popIdx))
                    if m == ["f"]:
                        return m
                    for k,v in m[0].items():
                        if foundMatches.get(k, v) != v:
                            return ["f"]
                        foundMatches[k] = v

        if ds != [] and not containsAtMatcher:
            return ["f"]

        for t in tuples:
            k,v = t
            if foundMatches.get(k, v) != v:
                return ["f"]
            foundMatches[k] = v

        return [foundMatches]

    def __instantiate(self, pattern, data):
        stk = []

        # When match doesn't match, 'f' is returned.
        # But instantiate requires a dictionary as data,
        # therefore we will propagate the error upwards.
        # This also has the adventage, that the equal?-rule:
        # Will implicitly return 'f' when the compared values wont match.
        if data == 'f':
            return data

        for matcher in pattern:
            match matcher:
                case str() if matcher.startswith('@'):
                    stk += data[matcher]
                case str() if matcher.startswith('#'):
                    stk += [data[matcher]]
                case _:
                    stk += [matcher]
        return stk
