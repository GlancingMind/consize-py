import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter

class Test(unittest.TestCase):

    def __test(self, ds, cs, result):
        i = Interpreter(rules=CONSIZE_RULE_SET, cs=cs, ds=ds)
        i.run()
        self.assertEqual(i.ds, result)

    def test_swap(self):
        self.__test(cs=["swap"], ds=["1","2","2","3"], result=["1","2","3","2"])

    def test_dup(self):
        self.__test(cs=["dup"], ds=["1","2","2","3"], result=["1","2","2","3","3"])

    def test_drop(self):
        self.__test(cs=["drop"], ds=["1","2","3"], result=["1","2"])

    def test_rot(self):
        self.__test(cs=["rot"], ds=["1","2","3","4"], result=["1","4","2","3"])

    def test_emptystack(self):
        self.__test(cs=["emptystack"], ds=[], result=[[]])
        self.__test(cs=["emptystack"], ds=["1","2"], result=["1","2",[]])

    def test_push(self):
        self.__test(cs=["push"], ds=["1","2","2",["4","3"],"5"], result=["1","2","2",["5","4","3"]])

    def test_top(self):
        self.__test(cs=["top"], ds=["1","2","2","3","nil"], result=["1","2","2","3","nil"])
        self.__test(cs=["top"], ds=["1","2","2","3",[]], result=["1","2","2","3","nil"])
        self.__test(cs=["top"], ds=["1","2","2","3",["a"]], result=["1","2","2","3","a"])
        self.__test(cs=["top"], ds=["1","2","2","3",["a","b"]], result=["1","2","2","3","a"])

    def test_pop(self):
        self.__test(cs=["pop"], ds=["1","2","2","3",[]], result=["1","2","2","3",[]])
        self.__test(cs=["pop"], ds=["1","2","2","3",["a"]], result=["1","2","2","3",[]])
        self.__test(cs=["pop"], ds=["1","2","2","3",["a","b"]], result=["1","2","2","3",["b"]])
        self.__test(cs=["pop"], ds=["1","2","2","3",["a","b","c"]], result=["1","2","2","3",["b","c"]])

    def test_unpush(self):
        self.__test(cs=["unpush"], ds=["1","2",[]], result=["1","2",[],"nil"])
        self.__test(cs=["unpush"], ds=["1","2",["a"]], result=["1","2",[],"a"])
        self.__test(cs=["unpush"], ds=["1","2",["a","b"]], result=["1","2",["b"],"a"])
        self.__test(cs=["unpush"], ds=["1","2",["a", "b", "c"]], result=["1","2",["b", "c"],"a"])

    def test_concat(self):
        self.__test(cs=["concat"], ds=[[],[]], result=[[]])
        self.__test(cs=["concat"], ds=[["a"],["b"]], result=[["a","b"]])
        self.__test(cs=["concat"], ds=[["a","b"],["c","d"]], result=[["a","b","c","d"]])

    def test_reverse(self):
        self.__test(cs=["reverse"], ds=[[]], result=[[]])
        self.__test(cs=["reverse"], ds=[["1"]], result=[["1"]])
        self.__test(cs=["reverse"], ds=[["1","2"]], result=[["2","1"]])
        self.__test(
            cs=["reverse"],
            ds=[["1",["2","3"],"4"]],
            result=[["4",["2","3"],"1"]])
