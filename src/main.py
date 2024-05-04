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
    """
    :return: New stack where the top element (here a stack) is replaced by it's
    first element, or "nil" when the top element is en empty stack or None.
    E.g: top(["a", [1, 2, 3, 4]]) returns [["a", 1]]
    """
    *rest, top = stack
    match top:
        case None | []: return rest + ["nil"]
        case _: return rest + [top[0]]

def pop(stack):
    """
    :return: New stack without the top most element.
    E.g.: pop([x y z]) returns [[x y]]
    """
    return stack[1:]

def concat(stack):
    """
    :return: New stack with the top two stacks concatenated into one.
    E.g.: concat([[a b c] [x y z]]) returns [[a b c x y z]]
    """
    *rest, stack1, stack2 = stack
    return rest + [ stack1 + stack2 ]

def reverse(stack):
    """
    :return: New stack in reversed order.
    E.g.: reverse([[a b c]]) returns [[c b a]]
    """
    return stack[::-1]

def mapping(stack):
    """
    :return: New stack with the top most stack converted to a dictionary.
    E.g.: mapping([[a 1 b 2 c 3]]) returns [{a:1, b: 2, c: 3}]
    """
    *rest, dictDescStack = stack
    keys = dictDescStack[0::2]
    values = dictDescStack[1::2]
    return rest + [{k: v for k,v in zip(keys, values)}]

def unmap(stack):
    """
    :return: New stack with the top most dictionary element converted to a stack.
    E.g.: unmap([{a:1, b: 2, c: 3}]) returns [[a 1 b 2 c 3]]
    """
    *rest, dictionary = stack
    return rest + [[element for item in dictionary.items() for element in item]]

def keys(stack):
    """
    :return: New stack with the top most dictionary on the stack being replaced
    by a stack containing the dictionaries keys.
    E.g.: keys([{a:1, b: 2, c: 3}]) returns [[a b c]]
    """
    *rest, dictionary = stack
    return rest + [ list(dictionary.keys()) ]

def assoc(stack):
    """
    :return: Add the value under the specified key into the top most dictionary
    of stack.
    E.g.: assoc([val key {a:1, b: 2, c: 3}]) returns [{a:1, b: 2, c: 3, key: value}]
    """
    *rest, key, value, dict = stack
    return rest + [ {**dict, key: value} ]

def dissoc(stack):
    """
    :return: New stack with the respective entry removed from the top most
    dictionary.
    E.g.: dissoc([c {a:1, b: 2, c: 3}]) returns [{a:1, b: 2}]
    """
    *rest, key, dict = stack
    return rest + [ {k: v for k, v in dict.items() if k != key} ]

def get(stack):
    """
    :return: New stack with the value of the dictionary as top element.
    E.g.: get([a {a:1, b: 2, c: 3} z]) returns [1] or when 'a' would existins in
    dictionary: ['z'].
    """
    *rest, key, dict, default = stack
    return rest + [ dict.get(key, default) ]
