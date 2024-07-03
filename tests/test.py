import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter

class Test(unittest.TestCase):

    def __test(self, initialStack, resultStack):
        output = Interpreter(rules=CONSIZE_RULE_SET, stack=initialStack).run()
        self.assertEqual(output, resultStack)

    def test_swap(self):
        self.__test(["1","2","2","3", "swap"],["1","2","3","2"])

    def test_dup(self):
        self.__test(["1","2","2","3", "dup"],["1","2","2","3","3"])

    def test_drop(self):
        self.__test(["1","2","2","3","drop"],["1","2","2"])

    def test_rot(self):
        self.__test(["1","2","3","4","rot"],["1","4","2","3"])

    def test_emptystack(self):
        self.__test(["1","2","2","3","emptystack"],["1","2","2","3",[]])

    def test_push(self):
        self.__test(["1","2","2","3",["4"],"5","push"],["1","2","2","3",["4","5"]])

    def test_top(self):
        self.__test(["1","2","2","3",["a"],"top"],["1","2","2","3","a"])
        self.__test(["1","2","2","3",["a", "b"],"top"],["1","2","2","3","a"])
        self.__test(["1","2","2","3",[],"top"],["1","2","2","3","nil"])
        self.__test(["1","2","2","3","nil","top"],["1","2","2","3","nil"])



    # def test_unpush(self):
    #     self.__test(["unpush", [], "1","2","2","3"],[[], "nil","1","2","2","3"])
    #     self.__test(["unpush", ["a"], "1","2","2","3"],["a","1","2","2","3"])
    #     self.__test(["unpush", ["a", "b"], "1","2","2","3"],["a","1","2","2","3"])
