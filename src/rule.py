from dataclasses import dataclass
from collections import ChainMap

@dataclass
class Rule:
    def __repr__(self) -> str:
        return self.ruleStr

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
        if pattern == [] and ds == []:
            return [{}]
        if pattern == []:
            return ["f"]

        if type(ds) != type(pattern):
            return ["f"]

        m = []
        matcher, *rstPat = pattern
        match matcher:
            case list():
                # if ds != list:
                #     return ["f"]
                word, *rstData = ds
                m += self.__match(rstPat, rstData) + self.__match(matcher, word)
                if "f" in m:
                    return ["f"]
                return [dict(ChainMap(*m))]
            case str() if matcher.startswith('@'):
                return [{ matcher: ds }]
            case str():
                if ds == []:
                    return ["f"]
                # nil ist ein Wort und wird hier aufgespalten! Das ist ein problem.
                word, *rstData = ds
                if matcher.startswith('#'):
                    m +=  self.__match(rstPat, rstData) + [{matcher: word}]
                elif word != matcher:
                    return ["f"]
                elif word == matcher:
                    m += self.__match(rstPat, rstData) + [{}]

        if "f" in m:
            return ["f"]
        if matcher in m[0].keys() and m[0][matcher] != word:
            return ["f"]
        return [dict(ChainMap(*m))]

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
