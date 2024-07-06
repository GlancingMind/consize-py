from dataclasses import dataclass
from sys import stderr

@dataclass
class Rule:
    def __repr__(self) -> str:
        return f"{self.mp} | {self.cs} -> {self.nds} | {self.ncs}"

    def __init__(self, mp, ocs, ip, ncs):
        self.mp = mp
        self.cs = ocs
        self.nds = ip
        self.ncs = ncs

    def execute(self, interpreter):
        csm = self.__match(self.cs, interpreter.cs)
        dsm = self.__match(self.mp, interpreter.ds)
        if csm == "f" or dsm == "f":
            return False
        matches = csm | dsm
        interpreter.cs = self.__instantiate(self.ncs, matches)
        interpreter.ds = self.__instantiate(self.nds, matches)
        return True

    def __match(self, pattern, ds):
        pattern = pattern.copy()
        # ds can also be a word (string) which doesn't have copy methode.
        ds = ds.copy() if isinstance(ds, list) else ds

        if pattern == [] and ds == []:
            return {}
        if pattern == []:
            return "f"
        if type(ds) != type(pattern):
            return "f"

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
                        return "f"
                    tuples.append((matcher, ds.pop(popIdx)))
                case str(): # Literal
                    if ds == []:
                        return "f"
                    e = ds.pop(popIdx)
                    if matcher != e:
                        return "f"
                case dict():
                    if ds == []:
                        return "f"
                    e = ds.pop(popIdx)
                    if matcher != e:
                        return "f"
                case list():
                    if ds == []:
                        return "f"
                    m = self.__match(matcher, ds.pop(popIdx))
                    if m == "f":
                        return m
                    for k,v in m.items():
                        if foundMatches.get(k, v) != v:
                            return "f"
                        foundMatches[k] = v

        if ds != [] and not containsAtMatcher:
            return "f"

        for t in tuples:
            k,v = t
            if foundMatches.get(k, v) != v:
                return "f"
            foundMatches[k] = v

        return foundMatches

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
                case list():
                    stk += [self.__instantiate(matcher, data)]
                case str() if matcher.startswith('@'):
                    stk += data[matcher]
                case str() if matcher.startswith('#'):
                    stk += [data[matcher]]
                case _:
                    stk += [matcher]
        return stk
