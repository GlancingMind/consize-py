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

    def test1(self):
        self.__test(["swap", "1","2","2","3"],["2","1","2","3"])

    def test2(self):
        self.__test(["emptystack", "1","2","2","3"],[[], "1","2","2","3"])

    def test3(self):
        self.__test(["top", ["a"], "1","2","2","3"],["a","1","2","2","3"])
        self.__test(["top", ["a", "b"], "1","2","2","3"],["a","1","2","2","3"])
        self.__test(["top", [], "1","2","2","3"],["nil","1","2","2","3"])
        self.__test(["top", "nil", "1","2","2","3"],["nil","1","2","2","3"])


