import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter
from Dictionary import Dictionary

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

    def test_equal(self):
        self.__test(cs=["equal?"], ds=["1","1"], result=["t"])
        self.__test(cs=["equal?"], ds=["1","2"], result=["f"])
        self.__test(cs=["equal?"], ds=["1","2","2"], result=["1","t"])
        self.__test(cs=["equal?"], ds=["1","2","3"], result=["1","f"])

    def test_identical(self):
        self.__test(cs=["identical?"], ds=["1","1"], result=["t"])
        self.__test(cs=["identical?"], ds=["1","2"], result=["f"])
        self.__test(cs=["identical?"], ds=["1","2","2"], result=["1","t"])
        self.__test(cs=["identical?"], ds=["1","2","3"], result=["1","f"])

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
        self.__test(cs=["concat"], ds=[["a","b"],["c","d"]], result=[["a","b","c","d"]])

    def test_escape(self):
        self.__test(cs=["a","\\"], ds=[], result=["a"])
        self.__test(cs=["a","\\"], ds=[[]], result=[[], "a"])
        self.__test(cs=["a","\\"], ds=["unchanged"], result=["unchanged", "a"])

    def test_reverse(self):
        self.__test(cs=["reverse"], ds=[[]], result=[[]])
        self.__test(cs=["reverse"], ds=[["1"]], result=[["1"]])
        self.__test(cs=["reverse"], ds=[["1","2"]], result=[["2","1"]])
        self.__test(
            cs=["reverse"],
            ds=[["1",["2","3"],"4"]],
            result=[["4",["2","3"],"1"]])

    def test_mapping(self):
        self.__test(cs=["mapping"], ds=[[]], result=[Dictionary()])
        self.__test(cs=["mapping"], ds=[["a","1"]], result=[Dictionary("a","1")])
        self.__test(cs=["mapping"], ds=[["a","1","b","2"]], result=[Dictionary("a","1","b","2")])
        self.__test(cs=["mapping"], ds=["unchanged", ["a","1","b","2"]], result=["unchanged", Dictionary("a","1","b","2")])

    def test_unmap(self):
        self.__test(cs=["unmap"], ds=[Dictionary()], result=[[]])
        self.__test(cs=["unmap"], ds=[Dictionary("a","1")], result=[["a","1"]])
        self.__test(cs=["unmap"], ds=[Dictionary("a","1", "b","2")], result=[["a","1","b","2"]])
        self.__test(cs=["unmap"], ds=["unchanged", Dictionary("a","1", "b","2")], result=["unchanged", ["a","1","b","2"]])

    def test_keys(self):
        self.__test(cs=["keys"], ds=["unchanged", Dictionary()], result=["unchanged", []])
        self.__test(cs=["keys"], ds=["unchanged", Dictionary("a","1")], result=["unchanged", ["a"]])
        self.__test(cs=["keys"], ds=["unchanged", Dictionary("a","1", "b","2")], result=["unchanged", ["a","b"]])

    def test_assoc(self):
        self.__test(cs=["assoc"], ds=["unchanged", "v", "k", Dictionary()], result=["unchanged", Dictionary("k", "v")])
        self.__test(cs=["assoc"], ds=["unchanged", "v", "k", Dictionary("k", "v")], result=["unchanged", Dictionary("k", "v")])
        self.__test(cs=["assoc"], ds=["unchanged", "b", "k", Dictionary("k", "v")], result=["unchanged", Dictionary("k", "b")])
        self.__test(cs=["assoc"], ds=["unchanged", "v2", "k2", Dictionary("k", "v")], result=["unchanged", Dictionary("k", "v", "k2", "v2")])
        self.__test(cs=["assoc"], ds=["unchanged", "changed", "k", Dictionary("x","z","k","b","a","v")], result=["unchanged", Dictionary("x","z","a","v","k","changed")])

    def test_get(self):
        self.__test(cs=["get"], ds=["unchanged", "k", Dictionary(), "d"], result=["unchanged", "d"])
        self.__test(cs=["get"], ds=["unchanged", "k", Dictionary("a","b"), "d"], result=["unchanged", "d"])
        self.__test(cs=["get"], ds=["unchanged", "k", Dictionary("a","b","c","e"), "d"], result=["unchanged", "d"])

        self.__test(cs=["get"], ds=["unchanged", "k", Dictionary("k","v"), "d"], result=["unchanged", "v"])
        self.__test(cs=["get"], ds=["unchanged", "k", Dictionary("a","v","k","b"), "d"], result=["unchanged", "b"])
        self.__test(cs=["get"], ds=["unchanged", "k", Dictionary("k","b","a","v"), "d"], result=["unchanged", "b"])
        self.__test(cs=["get"], ds=["unchanged", "k", Dictionary("x","z","k","b","a","v"), "d"], result=["unchanged", "b"])

    # def test_word(self):
    #     self.__test(cs=["word"], ds=[[]], result=["'","'"])
    #     self.__test(cs=["word"], ds=[["1"]], result=["'","1","'"])
    #     self.__test(cs=["word"], ds=[["1","2"]], result=[["'","1", "2","'"]])
