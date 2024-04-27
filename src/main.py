def wordstack(s) -> bool:
    """
    Determines if s is a list of strings - aka. a wordstack.

    :return: true, when s is a list of strings. Otherwise, false.
    """
    return isinstance(s, list) and s != [] and all(isinstance(item, str) for item in s)

def swap(stack):
    """
    """
    stack[-1], stack[-2] = stack[-2], stack[-1]

def dup(stack):
    """
    """
    stack +=  stack[-1]

