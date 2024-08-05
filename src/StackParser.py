from Stack import Dictionary, Stack

def parse(str: str):
    stk, _ = parse_stack(str)
    return stk

def parse_stack(str: str):
    pattern = Stack()
    tokens = str
    while tokens != []:
        token, *tokens = tokens
        if token == "[":
            p, tokens = parse_stack(tokens)
            pattern.append(p)
        elif token == "]":
            return Stack(*pattern), tokens
        elif token == "{":
            p, tokens = parse_dict(tokens)
            pattern.append(p)
        elif token.strip() == "":
            continue
        else:
            pattern.append(token)
    return pattern, tokens

def parse_dict(str: str):
    d = Dictionary()
    tokens = str
    while tokens != []:
        token, *tokens = tokens
        if token == "{":
            d, tokens = parse_dict(tokens)
            d.append(d)
        elif token == "}":
            break
        elif token.strip() == "":
            continue
        else:
            value, _ = parse_stack([token])
            # The result of __parsePattern will be always a stack.
            # Therefore __parsePattern([b]) for { a b }, will return [b].
            # But what we want is the unwrapped b, therefore we unwrap it.
            # What if { a [ b ] } is given?
            # Then __parsePattern will return
            # [[b]], which will be unwrapped, yielding the correct value [b].
            if len(value) == 1:
                d.append(value[0])
            else:
                d.append(value)
    return d, tokens
