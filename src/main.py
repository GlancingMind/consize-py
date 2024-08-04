#!/usr/bin/env python

import sys

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter
from Stack import Stack

# def apply(stack):
#     func, stk, *rest = stack
#     return [func(stk)] + rest

# def compose(stack):
#     funcO, funcI, *rest = stack
#     return [(lambda ds: funcO(funcI(ds)))] + rest

# def func(stack):
#     dict, quote, *rest = stack

#     def runcc(callstack, datastack, dict):
#         while callstack != []:
#             # callstack, datastack, dict = VM[toDictKey("stepcc")]([callstack, datastack, dict])
#             callstack, datastack, dict = stepcc([callstack, datastack, dict])
#         return datastack

#     return [lambda ds: runcc(callstack=quote, datastack=ds, dict=dict)] + rest

# def stepcc(stack):
#     callstack, datastack, dictionary, *rest = stack
#     itm, *rcs = callstack
#     match itm:
#         case str():
#             res = dictionary.get(toDictKey(itm), None)
#             match res:
#                 case list():
#                     return [res + rcs, datastack, dictionary] + rest
#                 case _ if callable(res):
#                     return [rcs, res(datastack), dictionary] + rest
#                 case _:
#                     return [["read-word"] + rcs, [itm] + datastack, dictionary] + rest
#         case dict():
#             return [["read-mapping"] + rcs, [itm] + datastack, dictionary] + rest
#         case _ if callable(itm):
#             return itm([rcs, datastack, dictionary] + rest)
#         case _:
#             return [rcs, [itm] + datastack, dictionary] + rest

# VM = {
#     "apply": apply,
#     "compose": compose,
#     "func": func,
# }

def main():
    # partialRunCC = func([VM, quotation])
    # datastack = []
    # result = apply(partialRunCC + [datastack])

    i = Interpreter(
        rules=CONSIZE_RULE_SET,
        cs=Stack("tokenize", "uncomment"),
        ds=Stack(" ".join(sys.argv[1:])))
    i.run()
    print("Consize returns", i.ds.toString())

if __name__ == "__main__":
    main()
