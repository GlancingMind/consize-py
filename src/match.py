from collections import ChainMap

def matches(ds: list, pattern: list):
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
            word, *rstData = ds
            m += matches(rstData, rstPat) + matches(word, matcher)
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
                m +=  matches(rstData, rstPat) + [{matcher: word}]
            elif word != matcher:
                return ["f"]
            elif word == matcher:
                m += matches(rstData, rstPat) + [{}]

    if "f" in m:
        return ["f"]
    if matcher in m[0].keys() and m[0][matcher] != word:
        return ["f"]
    return [dict(ChainMap(*m))]


def nm(ds: list, pattern: list):
    if pattern == [] and ds == []:
        return [{}]
    if pattern == []:
        return ["f"]
    if type(ds) != type(pattern):
        return ["f"]

    matches = {}
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
                m = nm(ds.pop(popIdx), matcher)
                for k,v in m[0].items():
                    if matches.get(k, v) != v:
                        return ["f"]
                    matches[k] = v

    if ds != [] and not containsAtMatcher:
        return ["f"]

    for t in tuples:
        k,v = t
        if matches.get(k, v) != v:
            return ["f"]
        matches[k] = v

    return [matches]

assert nm([{}],[{}]) == [{}], " "
assert nm([{"1":"Hello"}],[{"1":"Hello"}]) == [{}], " "
assert nm([{"1":"Hello"}],[{"1":"World"}]) == ["f"], " "
assert nm([{"2":"Hello"}],[{"1":"Hello"}]) == ["f"], " "
assert nm(["1","2","3","4"],["#F","#S","@M","#L"]) == [{"#F": "1", "#S": "2", "@M": ["3"], "#L": "4"}], ""
assert nm(["1","2","3","4","5"],["1","2","@T","#L"]) == [{"#L": "5", "@T": ["3","4"]}], ""
assert nm([],[]) == [{}], " "
assert nm(["1","2","3","4"],["1","2","3","4"]) == [{}], ""
assert nm(["1","2","3","4"],["1","2","3","1"]) == ["f"], ""
assert nm(["1","2","3","4"],["1","2","3"]) == ["f"], ""
assert nm(["1","2","3","4"],["@T"]) == [{"@T": ["1","2","3","4"]}], ""
assert nm([],["@T"]) == [{"@T": []}], ""
assert nm([],["#H"]) == ["f"], ""
assert nm([],["#H", "@T"]) == ["f"], ""
assert nm(["1"],["#F"]) == [{ "#F": "1"}], ""
assert nm(["1"],["#F", "#S"]) == ["f"], ""
assert nm(["1"],["#F", "@R"]) == [{"#F": "1", "@R": []}], ""
assert nm(["1",["2","3"], "4"],["#X", "#Y", "#Z"]) == [{"#X": "1", "#Y": ["2", "3"], "#Z": "4"}], ""
assert nm(["1",["2","3"], "4"],["#X", "@Y"]) == [{"#X": "1", "@Y": [["2", "3"], "4"]}], ""
assert nm(["1",["2","3"], "4"],["#X", "#Y", "#Z", "#U"]) == ["f"], ""
assert nm(["1","2","3"],["#X", "#Y", "#X"]) == ["f"], ""
assert nm(["1","2","1"],["#X", "#Y", "#X"]) == [{"#X": "1", "#Y": "2"}], ""
assert nm([["1",{"2": "3"},"4","5"],"6","7"],[["#F", "#S", "@R"], "@T"]) == [{ "#F": "1", "#S": { "2": "3" }, "@R": [ "4", "5" ], "@T": [ "6", "7" ] }], ""
assert nm([["1",{"2": "3"},"4","5"],"6","7"],["#1", "@2"]) == [{ "#1": ["1", { "2": "3" }, "4", "5" ], "@2": [ "6", "7" ] }], ""

# % test instantiate
# ( [ 1 2 3 ] ) [ { #H 1 @T [ 2 3 ] } [ #H @T ] instantiate ] unit-test
# ( [ 1 1 2 2 ] ) [ { #X 1 #Y 2 } [ #X 1 #Y 2 ] instantiate ] unit-test
# ( [ 4 4 2 3 ] ) [ { @T [ 2 3 ] #H 4 } [ #H #H @T ] instantiate ] unit-test
# % test rewrite
# ( [ y x z u v ] ) [ [ x y z u v ] [ #F #S @R ] [ #S #F @R ] rewrite ] unit-test
# ( f ) [ [ x ] [ #F #S @R ] [ #S #F @R ] rewrite ] unit-test