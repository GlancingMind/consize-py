# TODO can implement this as a strategy (in terms of strategy pattern)
# Which will be given to a rule via the RuleFactory, which will be initialized.
# Via commandline

def replace_prefix(prefix: str, nprefix: str, str: str):
    return nprefix+str.removeprefix(prefix)

def pattern_to_unpack_exp(pattern):
    transformed_pattern = []
    for word in pattern:
        match word:
            case list():
                transformed_pattern += [f"({pattern_to_unpack_exp(word)},)"]
            case str() if word.startswith("#"):
                transformed_pattern += [replace_prefix("#","H_",word)]
            case str() if word.startswith("@"):
                transformed_pattern += [replace_prefix("@","*AT_",word)]
            case _:
                transformed_pattern += [f"_{word}"]
    return (", ").join(transformed_pattern)

def match(pattern: str, stk: list):
    pattern = pattern_to_unpack_exp(pattern)

    try:
        exec(f"{pattern} = {stk}")
    except ValueError:
        return "f"

    matches = {}
    for k,v in locals().items():
        if k.startswith("H_"):
            matches[replace_prefix("H_","#",k)] = v
        elif k.startswith("AT_"):
            matches[replace_prefix("AT_","@",k)] = v
        elif k.startswith("_") and k.removeprefix("_") != str(v):
                return "f"
    return matches

# Example usage
stk = [1, [2, "hello", "world", [3], 4], 5]
matches = match(["#F", [2, "@GREETING", ["#NUM"], 4], "#L"], stk)
print(matches)
