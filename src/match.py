
def matches(ds: list, pattern: list):
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
                m = matches(ds.pop(popIdx), matcher)
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

assert matches([{}],[{}]) == [{}], " "
assert matches([{"1":"Hello"}],[{"1":"Hello"}]) == [{}], " "
assert matches([{"1":"Hello"}],[{"1":"World"}]) == ["f"], " "
assert matches([{"2":"Hello"}],[{"1":"Hello"}]) == ["f"], " "
assert matches(["1","2","3","4"],["#F","#S","@M","#L"]) == [{"#F": "1", "#S": "2", "@M": ["3"], "#L": "4"}], ""
assert matches(["1","2","3","4","5"],["1","2","@T","#L"]) == [{"#L": "5", "@T": ["3","4"]}], ""
assert matches([],[]) == [{}], " "
assert matches(["1","2","3","4"],["1","2","3","4"]) == [{}], ""
assert matches(["1","2","3","4"],["1","2","3","1"]) == ["f"], ""
assert matches(["1","2","3","4"],["1","2","3"]) == ["f"], ""
assert matches(["1","2","3","4"],["@T"]) == [{"@T": ["1","2","3","4"]}], ""
assert matches([],["@T"]) == [{"@T": []}], ""
assert matches([],["#H"]) == ["f"], ""
assert matches([],["#H", "@T"]) == ["f"], ""
assert matches(["1"],["#F"]) == [{ "#F": "1"}], ""
assert matches(["1"],["#F", "#S"]) == ["f"], ""
assert matches(["1"],["#F", "@R"]) == [{"#F": "1", "@R": []}], ""
assert matches(["1",["2","3"], "4"],["#X", "#Y", "#Z"]) == [{"#X": "1", "#Y": ["2", "3"], "#Z": "4"}], ""
assert matches(["1",["2","3"], "4"],["#X", "@Y"]) == [{"#X": "1", "@Y": [["2", "3"], "4"]}], ""
assert matches(["1",["2","3"], "4"],["#X", "#Y", "#Z", "#U"]) == ["f"], ""
assert matches(["1","2","3"],["#X", "#Y", "#X"]) == ["f"], ""
assert matches(["1","2","1"],["#X", "#Y", "#X"]) == [{"#X": "1", "#Y": "2"}], ""
assert matches([["1",{"2": "3"},"4","5"],"6","7"],[["#F", "#S", "@R"], "@T"]) == [{ "#F": "1", "#S": { "2": "3" }, "@R": [ "4", "5" ], "@T": [ "6", "7" ] }], ""
assert matches([["1",{"2": "3"},"4","5"],"6","7"],["#1", "@2"]) == [{ "#1": ["1", { "2": "3" }, "4", "5" ], "@2": [ "6", "7" ] }], ""

# % test instantiate
# ( [ 1 2 3 ] ) [ { #H 1 @T [ 2 3 ] } [ #H @T ] instantiate ] unit-test
# ( [ 1 1 2 2 ] ) [ { #X 1 #Y 2 } [ #X 1 #Y 2 ] instantiate ] unit-test
# ( [ 4 4 2 3 ] ) [ { @T [ 2 3 ] #H 4 } [ #H #H @T ] instantiate ] unit-test
# % test rewrite
# ( [ y x z u v ] ) [ [ x y z u v ] [ #F #S @R ] [ #S #F @R ] rewrite ] unit-test
# ( f ) [ [ x ] [ #F #S @R ] [ #S #F @R ] rewrite ] unit-test

# TODO Add instantiate to this module
# TODO Update Parser
# TODO should matchers also exist for dictionary content? E.g. { #X #Y @RI }
