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

def drop(stack):
    stack.pop()

def rot(stack):
    x, y, z = -1, -2, -3
    stack[x], stack[z], stack[y] = stack[z], stack[y], stack[x]

# TODO currently all values on the stack a basic words. Therefor stack, dict etc wont work.
def type(stack):
    match stack.pop():
        case str(): stack += ["wrd"]
        case list(): stack += ["stk"]
        case dict(): stack += ["map"]
        case function(): stack += ["fct"]
        #case nil: stack += ["nil"]
        case _: stack += ["_|_"]

def equal(stack):
    stack += "t" if stack.pop() == stack.pop() else "f"

def identical(stack):
    stack += "t" if stack.pop() is stack.pop() else "f"

def emptystack(stack):
    stack.append([])

def push(stack):
    top = stack.pop()
    stack[-1] += top

