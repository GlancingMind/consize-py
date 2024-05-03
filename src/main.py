import sys

def wordstack(s) -> bool:
    """
    Determines if s is a list of strings - aka. a wordstack.

    :return: true, when s is a list of strings. Otherwise, false.
    """
    return isinstance(s, list) and s != [] and all(isinstance(item, str) for item in s)

def swap(stack):
    """
    :return: New stack with the top two words swapped places.
    E.g: swap([x y]) returns [y x]
    """
    *rest, x, y = stack
    return rest + [y, x]

def dup(stack):
    """
    :return: New stack with the top word duplicated.
    E.g: swap([x]) returns [x x]
    """
    return stack + [stack[-1]]

def drop(stack):
    """
    :return: New stack with the top word removed.
    E.g: drop([x y z]) returns [x y]
    """
    return stack[:-1]

def rot(stack):
    """
    :return: New stack with the top three words rotated left-wise by one position.
    E.g.: rot([x y z]) returns [y z x]
    """
    *rest, x, y, z = stack
    return rest + [y, z, x]

def type(stack):
    """
    :return: New stack with the top element replaced by its type.
    E.g: type([x y z]) returns [x y wrd]
    """
    *rest, top = stack
    match top:
        case str():     return rest + ["wrd"]
        case list():    return rest + ["stk"]
        case dict():    return rest + ["map"]
        case _ if callable(top): return rest + ["fct"]
        case None:      return rest + ["nil"]
        case _:         return rest + ["_|_"]

def equal(stack):
    """
    :return: New stack with the two top elements replaced by their equality
    value: "t" when both are equal and "f" when they are not.
    E.g: equal([x y]) returns [f]
    """
    *rest, x, y = stack
    return rest + ["t" if x == y else "f"]

def identical(stack):
    """
    :return: New stack with the two top elements replaced by their identity-equality.
    E.g: identical([x y]) returns [f]
    Note: This function is the same as equality and not required for a
    functioning consize implementation. See respective documentation in
    consize.pdf.
    """
    return equal(stack)

def emptystack(stack):
    """
    :return: New stack with an empty stack as top element.
    E.g: emptystack([]) returns [[]] or emptystack(["a"]) returns ["a", []]
    """
    return stack + [[]]

def push(stack):
    """
    :return: New stack with the top most element pushed into the below sitting stack.
    E.g: push([[], "a"]) returns [["a"]]
    """
    *rest, stk, top = stack
    return rest + [stk + [top]]

def top(stack):

    match stack[-1]:
        case "nil" | []: stack[-1] = "nil"
        case list(): stack[-1] = stack[-1][0]
        case _: print(f"error: stack underflow for {stack[-1]}", file=sys.stderr)

def pop(stack):
    return stack[1:]

def concat(stack):
    return stack[:-2] + [ stack[-2] + stack[-1] ]

def reverse(stack):
    # Could also use stack.reverse(), but this would mutate the stack.
    # Following code reverses the stack without mutating the given one.
    return stack[::-1]

def mapping(stack):
    dictDesc = stack[-1]
    return stack[:-1] + [{k: v for k,v in zip(dictDesc[0::2], dictDesc[1::2])}]

def unmap(stack):
    dictionary = stack[-1]
    return stack[:-1] + [[element for item in dictionary.items() for element in item]]

def keys(stack):
    return stack[:-1] + [ list(stack[-1].keys()) ]

def assoc(stack):
    *rest, key, value, dict = stack
    return rest + [ {**dict, key: value} ]
