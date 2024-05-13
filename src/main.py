#!/usr/bin/env python

import sys

def isWordstack(s) -> bool:
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
    x, y, *rest, = stack
    return [y, x] + rest

def dup(stack):
    """
    :return: New stack with the top word duplicated.
    E.g: swap([x]) returns [x x]
    """
    top, *rest = stack
    return [top, top] + rest

def drop(stack):
    """
    :return: New stack with the top word removed.
    E.g: drop([x y z]) returns [x y]
    """
    top, *rest = stack
    return rest

def rot(stack):
    """
    :return: New stack with the top three words rotated left-wise by one position.
    E.g.: rot([x y z]) returns [y z x]
    """
    x, y, z, *rest = stack
    return [z, x, y] + rest

def type(stack):
    """
    :return: New stack with the top element replaced by its type.
    E.g: type([x y z]) returns [x y wrd]
    """
    top, *rest = stack
    match top:
        case str():     return ["wrd"] + rest
        case list():    return ["stk"] + rest
        case dict():    return ["map"] + rest
        case _ if callable(top): return ["fct"] + rest
        case None:      return ["nil"] + rest
        case _:         return ["_|_"] + rest

def equal(stack):
    """
    :return: New stack with the two top elements replaced by their equality
    value: "t" when both are equal and "f" when they are not.
    E.g: equal([x y]) returns [f]
    """
    x, y, *rest = stack
    return ["t" if x == y else "f"] + rest

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
    return [[]] + stack

def push(stack):
    """
    :return: New stack with the top most element pushed into the below sitting stack.
    E.g: push([[], "a"]) returns [["a"]]
    """
    top, stk, *rest = stack
    return [[top] + stk] + rest

def top(stack):
    """
    :return: New stack where the top element (here a stack) is replaced by it's
    first element, or "nil" when the top element is en empty stack or None.
    E.g: top(["a", [1, 2, 3, 4]]) returns [["a", 1]]
    """
    top, *rest = stack
    match top:
        case "nil": print("error: top cannot be used on nil")
        case None | []: return [None] + rest
        case _: return [top[0]] + rest

def pop(stack):
    """
    :return: New stack without the top most element.
    E.g.: pop([x y z]) returns [[x y]]
    """
    innerStack, *rest = stack
    if isinstance(innerStack, str):
        print(f"error: '{innerStack}' isnt a stack. Did not perform pop. Current stack is:")
        return stack
    if innerStack == None:
        return [[]] + rest
    return [innerStack[1:]] + rest

def concat(stack):
    """
    :return: New stack with the top two stacks concatenated into one.
    E.g.: concat([[a b c] [x y z]]) returns [[a b c x y z]]
    """
    stack1, stack2, *rest = stack
    return [ stack2 + stack1 ] + rest

def reverse(stack):
    """
    :return: New stack in reversed order.
    E.g.: reverse([[a b c]]) returns [[c b a]]
    """
    stk, *rest = stack
    return [stk[::-1]] + rest

def mapping(stack):
    """
    :return: New stack with the top most stack converted to a dictionary.
    E.g.: mapping([[a 1 b 2 c 3]]) returns [{a:1, b: 2, c: 3}]
    """
    dictDescStack, *rest = stack
    keys = dictDescStack[0::2]
    values = dictDescStack[1::2]
    return [{toDictKey(k): v for k,v in zip(keys, values)}] + rest

def unmap(stack):
    """
    :return: New stack with the top most dictionary element converted to a stack.
    E.g.: unmap([{a:1, b: 2, c: 3}]) returns [[a 1 b 2 c 3]]
    """
    dictionary, *rest = stack
    return [[element for item in dictionary.items() for element in item]] + rest

def keys(stack):
    """
    :return: New stack with the top most dictionary on the stack being replaced
    by a stack containing the dictionaries keys.
    E.g.: keys([{a:1, b: 2, c: 3}]) returns [[a b c]]
    """
    dictionary, *rest = stack
    return [ [restoreDictKey(k) for k in dictionary.keys()] ] + rest

def assoc(stack):
    """
    :return: Add the value under the specified key into the top most dictionary
    of stack.
    E.g.: assoc([val key {a:1, b: 2, c: 3}]) returns [{a:1, b: 2, c: 3, key: value}]
    """
    dict, key, value, *rest = stack
    return [ {**dict, toDictKey(key): value} ] + rest

def dissoc(stack):
    """
    :return: New stack with the respective entry removed from the top most
    dictionary.
    E.g.: dissoc([c {a:1, b: 2, c: 3}]) returns [{a:1, b: 2}]
    """
    dict, key, *rest = stack
    key = toDictKey(key)
    return [ {k: v for k, v in dict.items() if k != key} ] + rest

def toDictKey(obj):
    return str(f"{obj}")

def restoreDictKey(key):
    import ast
    return ast.literal_eval(key)

def get(stack):
    """
    :return: New stack with the value of the dictionary as top element.
    E.g.: get([a {a: 1, b: 2, c: 3} z]) returns [1] or when 'a' would exist in
    dictionary: ['z'].
    """
    default, dictionary, key, *rest = stack
    return [ dictionary.get(toDictKey(key), default) ] + rest

def merge(stack):
    """
    :return: New stack with the top two dictionaries merges into one.
    E.g.: merge([{a: 1, b: 2} {a:2, c: 3}]) returns [{a: 2, b: 2, c: 3}].
    """
    dict1, dict2, *rest = stack
    return [ dict2 | dict1 ] + rest

def word(stack):
    """
    :return: New stack with all word within the top most wordstack compressed
    into one continues word.
    E.g.: word([["it's", "me", "!"]]) returns ["it'sme!"].
    """
    wordstack, *rest = stack
    return ["".join(wordstack)] + rest

def unword(stack):
    word, *rest = stack
    return [[character for character in word]] + rest

def char(stack):
    """
    :return: New stack with the top most element being the interpreted
    character.

    NOTE: Top element on the stack should be a raw string, otherwise
    interpretation will fail.

    E.g: char([r"\\u0040"]) will return ["@"]
         char([r"\\o100"]) will return ["@"]
    """
    characterCode, *rest = stack
    match characterCode:
        case r"\space":     return [" "] + rest
        case r"\newline":   return ["\n"] + rest
        case r"\formfeed":  return ["\f"] + rest
        case r"\return":    return ["\r"] + rest
        case r"\backspace": return ["\b"] + rest
        case r"\tab":       return ["\t"] + rest
        case _ if characterCode.startswith(r"\o"):
            return [chr(int(characterCode[2:], 8))] + rest
        case _ if characterCode.startswith(r"\u"):
            return [bytes(characterCode, "utf-8").decode("unicode_escape")] + rest
        case _:
            return [fr"error: {characterCode} isn't a valid character codec"] + rest

def _print(stack):
    word, *rest = stack
    print(word, end="") if isinstance(word, str) else print("error: top element isn't of type string")
    return rest

def flush(stack):
    sys.stdout.flush()
    return stack

def readLine(stack):
    return [input()] + stack

def slurp(stack):
    from urllib.parse import urlparse
    import requests
    from requests_file import FileAdapter

    session = requests.Session()
    session.mount('file://', FileAdapter())

    source, *rest = stack

    if(urlparse(source).scheme == ""):
        # seems to be not a valid URI. Will use local file read.
        try:
            with open(source, "r") as file:
                return [file.read()] + rest
        except FileNotFoundError:
            print("File not found:", source)
        except PermissionError:
            print("Permission denied to read file:", source)
        except IOError as e:
            print("An error occurred while reading the file:", e)
    else:
        # some URI schema was detected will try fetching remote resource.
        try:
            response = session.get(r""+source)
            if response.status_code == 200:
                return [response.text] + rest
            else:
                print("Error:", response.status_code)
                return rest
        except requests.RequestException as e:
            print("error:", e)
            return rest
    return rest

def spit(stack):
    from urllib.parse import urlparse

    uri, data, *rest = stack

    pr = urlparse(uri)
    if(pr.scheme == "file" or pr.scheme == ""):
        # seems to be not a valid URI. Will use local file read.
        try:
            with open(pr.path, "w") as file:
                file.write(data)
        except FileNotFoundError:
            print("File not found:", pr.path)
        except PermissionError:
            print("Permission denied to write file:", pr.path)
        except IOError as e:
            print("An error occurred while writing the file:", e)
    return rest

def spitOn(stack):
    from urllib.parse import urlparse

    uri, data, *rest = stack

    pr = urlparse(uri)
    if(pr.scheme == "file" or pr.scheme == ""):
        # seems to be not a valid URI. Will use local file read.
        try:
            with open(pr.path, "a") as file:
                file.write(data)
        except FileNotFoundError:
            print("File not found:", pr.path)
        except PermissionError:
            print("Permission denied to write file:", pr.path)
        except IOError as e:
            print("An error occurred while writing the file:", e)
    return rest

def uncomment(stack):
    import re
    word, *rest = stack
    parts = re.split(r"\s*%.*[(\r\n)\r\n]", word)
    # parts = re.split(r"(?m)\s*%.*$", word)

    # TODO last newline is kept and printed when using uncomment

    return ["\r\n".join(parts)] + rest

def tokenize(stack):
    import re
    word, *rest = stack
    parts = re.split(r"\s+", word.strip())
    return ([] if parts == [""] else [parts]) + rest

def undocument(stack):
    import re
    word, *rest = stack
    parts = re.findall(r"(?m)^%?>> (.*)$", word)
    return ["\r\n".join(parts)] + rest

def currentTimeInMilliSeconds(stack):
    import time
    return [int(time.time() * 1000)] + stack

def operatingSystem(stack):
    import platform
    return [platform.platform()] + stack

def apply(stack):
    func, stk, *rest = stack
    return [func(stk)] + rest

def compose(stack):
    funcO, funcI, *rest = stack
    return [(lambda ds: funcO(funcI(ds)))] + rest

def func(stack):
    dict, quote, *rest = stack

    def runcc(callstack, datastack, dict):
        while callstack != []:
            # callstack, datastack, dict = VM[toDictKey("stepcc")]([callstack, datastack, dict])
            callstack, datastack, dict = stepcc([callstack, datastack, dict])
        return datastack

    return [lambda ds: runcc(callstack=quote, datastack=ds, dict=dict)] + rest

counter = 1
def stepcc(stack):
    callstack, datastack, dictionary, *rest = stack
    itm, *rcs = callstack

    global counter
    print(f"{counter} Cs: {callstack}\nDs: {datastack}")
    counter = counter + 1

    match itm:
        case str():
            res = dictionary.get(toDictKey(itm), None)
            match res:
                case list():
                    return [res + rcs, datastack, dictionary] + rest
                case _ if callable(res):
                    return [rcs, res(datastack), dictionary] + rest
                case _:
                    return [["read-word"] + rcs, [itm] + datastack, dictionary] + rest
        case dict():
            return [["read-mapping"] + rcs, [itm] + datastack, dictionary] + rest
        case _ if callable(itm):
            return itm([rcs, datastack, dictionary] + rest)
        case _:
            return [rcs, [itm] + datastack, dictionary] + rest

def call(stack):
    callstack, datastack, *rest = stack
    if datastack == []: return [callstack] + [[]] + rest
    dsHead, *dsTail = datastack
    if not isinstance(dsHead, list):
        dsHead = [dsHead]
    return [dsHead + callstack] + [dsTail] + rest

def quote(stack):
    callstack, datastack, *rest = stack
    dsHead, *dsTail = datastack
    csHead, *csTail = callstack or ([],[])
    return [["call"] + csTail] + [dsTail + [csHead, dsHead]] + rest

def callCC(stack):
    callstack, datastack, *rest = stack
    dsHead, *dsTail = datastack
    return [dsHead] + [[callstack, dsTail]] + rest

def continuee(stack):
    callstack, datastack, *rest = stack
    newCallStack, newDataStack, *rds = datastack
    return [newCallStack] + [newDataStack] + rest

def getDict(stack):
    callstack, datastack, dict, *rest = stack
    return [callstack, [dict] + datastack, dict] + rest

def setDict(stack):
    callstack, datastack, dict, *rest = stack
    dsHead, *dsTail = datastack
    return [callstack, dsTail, dsHead] + rest

def integer(stack):
    word, *rest = stack

    if isinstance(word, int):
        return ["t"] + rest

    # check if a given string represents an integer
    if word == str() and word.startswith('-'):
       word = word[1:] # remove the minus from string

    return ["t" if word.isdigit() else "f"] + rest

def plus(stack):
    y, x, *rest = stack
    return [str(int(x)+int(y))] + rest

def minus(stack):
    y, x, *rest = stack
    return [str(int(x)-int(y))] + rest

def multiply(stack):
    y, x, *rest = stack
    return [str(int(x)*int(y))] + rest

def divide(stack):
    y, x, *rest = stack
    return [str(int(x)//int(y))] + rest

def modulus(stack):
    y, x, *rest = stack
    return [str(int(x)%int(y))] + rest

def lessThan(stack):
    y, x, *rest = stack
    return ["t" if int(x) < int(y) else "f"] + rest

def moreThan(stack):
    y, x, *rest = stack
    return ["t" if int(x) > int(y) else "f"] + rest

def lessThanEqual(stack):
    y, x, *rest = stack
    return ["t" if int(x) <= int(y) else "f"] + rest

def moreThanEqual(stack):
    y, x, *rest = stack
    return ["t" if int(x) >= int(y) else "f"] + rest

VM = {
    toDictKey("swap"): swap,
    toDictKey("dup"): dup,
    toDictKey("drop"): drop,
    toDictKey("rot"): rot,
    toDictKey("type"): type,
    toDictKey("equal?"): equal,
    toDictKey("identical?"): identical,
    toDictKey("emptystack"): emptystack,
    toDictKey("push"): push,
    toDictKey("top"): top,
    toDictKey("pop"): pop,
    toDictKey("concat"): concat,
    toDictKey("reverse"): reverse,
    toDictKey("mapping"): mapping,
    toDictKey("unmap"): unmap,
    toDictKey("keys"): keys,
    toDictKey("assoc"): assoc,
    toDictKey("dissoc"): dissoc,
    toDictKey("get"): get,
    toDictKey("merge"): merge,
    toDictKey("word"): word,
    toDictKey("unword"): unword,
    toDictKey("char"): char,
    toDictKey("print"): _print,
    toDictKey("flush"): flush,
    toDictKey("read-line"): readLine,
    toDictKey("slurp"): slurp,
    toDictKey("spit"): spit,
    toDictKey("spit-on"): spitOn,
    toDictKey("uncomment"): uncomment,
    toDictKey("tokenize"): tokenize,
    toDictKey("undocument"): undocument,
    toDictKey("current-time-millis"): currentTimeInMilliSeconds,
    toDictKey("operating-system"): operatingSystem,
    toDictKey("call"): [call],
    # toDictKey("quote"): [quote],
    toDictKey("call/cc"): [callCC],
    toDictKey("continue"): [continuee],
    toDictKey("get-dict"): [getDict],
    toDictKey("set-dict"): [setDict],
    toDictKey("stepcc"): stepcc,
    toDictKey("apply"): apply,
    toDictKey("compose"): compose,
    toDictKey("func"): func,
    toDictKey("integer?"): integer,
    toDictKey("+"): plus,
    toDictKey("-"): minus,
    toDictKey("*"): multiply,
    toDictKey("div"): divide,
    toDictKey("mod"): modulus,
    toDictKey("<"): lessThan,
    toDictKey(">"): moreThan,
    toDictKey("=="): equal,
    toDictKey("<="): lessThanEqual,
    toDictKey(">="): moreThanEqual,
    # toDictKey("\\"):   [["top"], "quote"],
    toDictKey("\\"):   [["dup", "top", "rot", "swap", "push", "swap", "pop", "continue"], "call/cc"],
    toDictKey("load"): ["slurp", "uncomment", "tokenize"],
    toDictKey("run"):  ["load", "call"],
    toDictKey("start"): ["slurp", "uncomment", "tokenize", "get-dict", "func", "emptystack", "swap", "apply"],
}

def main():
    joinedArgs = " ".join(sys.argv[1:])
    wrappedQuotation = tokenize(uncomment([joinedArgs]))
    quotation = wrappedQuotation[0]
    partialRunCC = func([VM, quotation])
    datastack = []
    result = apply(partialRunCC + [datastack])
    print("Consize returns", result[0])

if __name__ == "__main__":
    from functools import partial

    # def log(k, f, s):
    #    print(f"[\033[1m{k}\033[0m] called with \033[31m{s}\033[0m")
    #    result = f(s)
    #    print(f"[\033[1m{k}\033[0m] returned: \033[32m{result}\033[0m")

    # for k,f in VM.items():
    #    VM[k] = partial(log, k, f)

    main()
