#!/usr/bin/env python

import sys
from dataclasses import dataclass

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter
from RuleSet import RuleSet

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
    return [re.sub(r"(?m)\s*%.*$", "", word).strip()] + rest

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

def stepcc(stack):
    callstack, datastack, dictionary, *rest = stack
    itm, *rcs = callstack
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
    # Dict functions
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
    # toDictKey("=="): equal,
    toDictKey("<="): lessThanEqual,
    toDictKey(">="): moreThanEqual,

    # toDictKey("\\"):   [["top"], "quote"],
    toDictKey("\\"):   [["dup", "top", "rot", "swap", "push", "swap", "pop", "continue"], "call/cc"],
    toDictKey("load"): ["slurp", "uncomment", "tokenize"],
    toDictKey("run"):  ["load", "call"],
    toDictKey("start"): ["slurp", "uncomment", "tokenize", "get-dict", "func", "emptystack", "swap", "apply"],
    # toDictKey("match"): matches,
    # toDictKey("instantiate"): instantiate,
    toDictKey("rewrite"): ["[", "match", "]", "dip", "over", "[", "instantiate", "]", "[", "drop", "]", "if"],
}

def main():
    initialStack = ["swap", "1","2","2","3"]
    # initialStack = ["emptystack", "1","2","2","3"]
    # initialStack = ["top", ["a", "b"], "1","2","2","3"]
    # initialStack = ["top", [], "1","2","2","3"]
    # initialStack = ["top", "nil", "1","2","2","3"]
    i = Interpreter(rules=CONSIZE_RULE_SET, stack=initialStack)
    i.run()
    i.printState()
    # joinedArgs = " ".join(sys.argv[1:])
    # wrappedQuotation = tokenize(uncomment([joinedArgs]))
    # quotation = wrappedQuotation[0]
    # partialRunCC = func([VM, quotation])
    # datastack = []
    # result = apply(partialRunCC + [datastack])
    # print("Consize returns", result[0])

if __name__ == "__main__":
    main()
