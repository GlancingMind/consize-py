from io import StringIO
import sys
import unittest
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ConsizeRuleSet import CONSIZE_RULE_SET
from Interpreter import Interpreter
from Stack import Dictionary, Stack


class Test(unittest.TestCase):

    def __test(self, ds, cs, result):
        i = Interpreter(rules=CONSIZE_RULE_SET, cs=cs, ds=ds)
        i.run()
        self.assertEqual(i.ds, result)

    def test_swap(self):
        self.__test(cs=Stack("swap"), ds=Stack("1","2","2","3"), result=Stack("1","2","3","2"))

    def test_dup(self):
        self.__test(cs=Stack("dup"), ds=Stack("1","2","2","3"), result=Stack("1","2","2","3","3"))

    def test_drop(self):
        self.__test(cs=Stack("drop"), ds=Stack("1","2","3"), result=Stack("1","2"))

    def test_rot(self):
        self.__test(cs=Stack("rot"), ds=Stack("1","2","3","4"), result=Stack("1","4","2","3"))

    def test_equal(self):
        self.__test(cs=Stack("equal?"), ds=Stack("1","1"), result=Stack("t"))
        self.__test(cs=Stack("equal?"), ds=Stack("1","2"), result=Stack("f"))
        self.__test(cs=Stack("equal?"), ds=Stack("1","2","2"), result=Stack("1","t"))
        self.__test(cs=Stack("equal?"), ds=Stack("1","2","3"), result=Stack("1","f"))

    def test_identical(self):
        self.__test(cs=Stack("identical?"), ds=Stack("1","1"), result=Stack("t"))
        self.__test(cs=Stack("identical?"), ds=Stack("1","2"), result=Stack("f"))
        self.__test(cs=Stack("identical?"), ds=Stack("1","2","2"), result=Stack("1","t"))
        self.__test(cs=Stack("identical?"), ds=Stack("1","2","3"), result=Stack("1","f"))

    def test_emptystack(self):
        self.__test(cs=Stack("emptystack"), ds=Stack(), result=Stack(Stack()))
        self.__test(cs=Stack("emptystack"), ds=Stack("1","2"), result=Stack("1","2",Stack()))

    def test_push(self):
        self.__test(cs=Stack("push"), ds=Stack("1","2","2",Stack("4","3"),"5"), result=Stack("1","2","2",Stack("5","4","3")))

    def test_top(self):
        self.__test(cs=Stack("top"), ds=Stack("1","2","2","3","nil"), result=Stack("1","2","2","3","nil"))
        self.__test(cs=Stack("top"), ds=Stack("1","2","2","3",Stack()), result=Stack("1","2","2","3","nil"))
        self.__test(cs=Stack("top"), ds=Stack("1","2","2","3",Stack("a")), result=Stack("1","2","2","3","a"))
        self.__test(cs=Stack("top"), ds=Stack("1","2","2","3",Stack("a","b")), result=Stack("1","2","2","3","a"))

    def test_pop(self):
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack()), result=Stack("1","2","2","3",Stack()))
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack("a")), result=Stack("1","2","2","3",Stack()))
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack("a","b")), result=Stack("1","2","2","3",Stack("b")))
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack("a","b","c")), result=Stack("1","2","2","3",Stack("b","c")))

    def test_unpush(self):
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack()), result=Stack("1","2",Stack(), "nil"))
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack("a")), result=Stack("1","2",Stack(),"a"))
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack("a","b")), result=Stack("1","2",Stack("b"),"a"))
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack("a", "b", "c")), result=Stack("1","2",Stack("b", "c"),"a"))

    def test_concat(self):
        self.__test(cs=Stack("concat"), ds=Stack(Stack(),Stack()), result=Stack(Stack()))
        self.__test(cs=Stack("concat"), ds=Stack(Stack("a"),Stack("b")), result=Stack(Stack("a","b")))
        self.__test(cs=Stack("concat"), ds=Stack(Stack("a","b"), Stack("c","d")), result=Stack(Stack("a","b","c","d")))

    def test_escape(self):
        self.__test(cs=Stack("a","\\"), ds=Stack(), result=Stack("a"))
        self.__test(cs=Stack("a","\\"), ds=Stack(Stack()), result=Stack(Stack(), "a"))
        self.__test(cs=Stack("a","\\"), ds=Stack("unchanged"), result=Stack("unchanged", "a"))

    def test_reverse(self):
        self.__test(cs=Stack("reverse"), ds=Stack(Stack()), result=Stack(Stack()))
        self.__test(cs=Stack("reverse"), ds=Stack(Stack("1")), result=Stack(Stack("1")))
        self.__test(cs=Stack("reverse"), ds=Stack(Stack("1","2")), result=Stack(Stack("2","1")))
        self.__test(cs=Stack("reverse"), ds=Stack(Stack("1",Stack("2","3"),"4")), result=Stack(Stack("4",Stack("2","3"),"1")))

    def test_mapping(self):
        self.__test(cs=Stack("mapping"), ds=Stack(Stack()), result=Stack(Dictionary()))
        self.__test(cs=Stack("mapping"), ds=Stack(Stack("a","1")), result=Stack(Dictionary("a","1")))
        self.__test(cs=Stack("mapping"), ds=Stack(Stack("a","1","b","2")), result=Stack(Dictionary("a","1","b","2")))
        self.__test(cs=Stack("mapping"), ds=Stack("unchanged", Stack("a","1","b","2")), result=Stack("unchanged", Dictionary("a","1","b","2")))

    def test_unmap(self):
        self.__test(cs=Stack("unmap"), ds=Stack(Dictionary()), result=Stack(Stack()))
        self.__test(cs=Stack("unmap"), ds=Stack(Dictionary("a","1")), result=Stack(Stack("a","1")))
        self.__test(cs=Stack("unmap"), ds=Stack(Dictionary("a","1", "b","2")), result=Stack(Stack("a","1","b","2")))
        self.__test(cs=Stack("unmap"), ds=Stack("unchanged", Dictionary("a","1", "b","2")), result=Stack("unchanged", Stack("a","1","b","2")))

    def test_keys(self):
        self.__test(cs=Stack("keys"), ds=Stack("unchanged", Dictionary()), result=Stack("unchanged", Stack()))
        self.__test(cs=Stack("keys"), ds=Stack("unchanged", Dictionary("a","1")), result=Stack("unchanged", Stack("a")))
        self.__test(cs=Stack("keys"), ds=Stack("unchanged", Dictionary("a","1", "b","2")), result=Stack("unchanged", Stack("a","b")))

    def test_assoc(self):
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "v", "k", Dictionary()), result=Stack("unchanged", Dictionary("k", "v")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "v", "k", Dictionary("k", "v")), result=Stack("unchanged", Dictionary("k", "v")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "b", "k", Dictionary("k", "v")), result=Stack("unchanged", Dictionary("k", "b")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "v2", "k2", Dictionary("k", "v")), result=Stack("unchanged", Dictionary("k", "v", "k2", "v2")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "changed", "k", Dictionary("x","z","k","b","a","v")), result=Stack("unchanged", Dictionary("x","z","a","v","k","changed")))

    def test_dissoc(self):
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "k", Dictionary()), result=Stack("unchanged", Dictionary()))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "k", Dictionary("k", "v")), result=Stack("unchanged", Dictionary()))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "x", Dictionary("x","z","k","b","a","v")), result=Stack("unchanged", Dictionary("k","b","a","v")))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "k", Dictionary("x","z","k","b","a","v")), result=Stack("unchanged", Dictionary("x","z","a","v")))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "a", Dictionary("x","z","k","b","a","v")), result=Stack("unchanged", Dictionary("x","z","k","b")))

    def test_get(self):
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary(), "d"), result=Stack("unchanged", "d"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("a","b"), "d"), result=Stack("unchanged", "d"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("a","b","c","e"), "d"), result=Stack("unchanged", "d"))

        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("k","v"), "d"), result=Stack("unchanged", "v"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("a","v","k","b"), "d"), result=Stack("unchanged", "b"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("k","b","a","v"), "d"), result=Stack("unchanged", "b"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("x","z","k","b","a","v"), "d"), result=Stack("unchanged", "b"))

    def test_merge(self):
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary(), Dictionary()), result=Stack("unchanged", Dictionary()))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary(), Dictionary("k", "v")), result=Stack("unchanged", Dictionary("k","v")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("k", "v"), Dictionary()), result=Stack("unchanged", Dictionary("k","v")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("x","z","k","b"), Dictionary("a","v")), result=Stack("unchanged", Dictionary("x","z", "k","b", "a","v")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("x","z"), Dictionary("k","b","a","v")), result=Stack("unchanged", Dictionary("x","z", "a","v", "k","b")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("a","z", "k","b", "e","x"), Dictionary("a","changed",)), result=Stack("unchanged", Dictionary("k","b", "e","x", "a","changed")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("a","z", "k","b", "e","x"), Dictionary("k","changed",)), result=Stack("unchanged", Dictionary("a","z", "e","x", "k","changed")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("a","z", "k","b", "e","x"), Dictionary("e","changed",)), result=Stack("unchanged", Dictionary("a","z", "k","b", "e","changed")))

    def test_unword(self):
        self.__test(cs=Stack("unword"), ds=Stack(), result=Stack())
        self.__test(cs=Stack("unword"), ds=Stack("unchanged", "Hello"), result=Stack("unchanged", Stack("H","e","l","l","o")))

    def test_word(self):
        self.__test(cs=Stack("word"), ds=Stack(Stack("1")), result=Stack("1"))
        self.__test(cs=Stack("word"), ds=Stack("unchanged", Stack("1","2")), result=Stack("unchanged", "12"))

    def test_char(self):
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\space"), result=Stack("unchanged", " "))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\newline"), result=Stack("unchanged", "\n"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\formfeed"), result=Stack("unchanged","\f"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\return"), result=Stack("unchanged","\r"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\backspace"), result=Stack("unchanged","\b"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\tab"), result=Stack("unchanged","\t"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\u0040"), result=Stack("unchanged","@"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\o100"), result=Stack("unchanged","@"))

    def test_print(self):
        self.__test(cs=Stack("print"), ds=Stack("Hello World"), result=Stack())

    def test_readline(self):
        from contextlib import contextmanager

        @contextmanager
        def replace_stdin(target):
            orig = sys.stdin
            sys.stdin = target
            yield
            sys.stdin = orig
        with replace_stdin(StringIO("Some preprogrammed input")):
            self.__test(cs=Stack("read-line"), ds=Stack(), result=Stack("Some preprogrammed input"))

    def test_slurp(self):
        self.__test(cs=Stack("slurp"), ds=Stack("./tests/test-file-for-slurp.txt"), result=Stack("Hello Consize!\n"))

    def test_spit(self):
        filePath = "./tests/test-file-for-spit.txt"
        with open(filePath, "w") as file:
            file.write("")
        self.__test(cs=Stack("spit"), ds=Stack("unchanged", "Hello Consize!\n", filePath), result=Stack("unchanged"))
        content = ""
        with open(filePath, "r") as file:
            content = file.read()
        self.assertEqual(content, "Hello Consize!\n")

    def test_spit_on(self):
        filePath = "./tests/test-file-for-spit-on.txt"
        data = "Hello You!\n"
        with open(filePath, "w") as file:
            file.write(data)
        self.__test(cs=Stack("spit-on"), ds=Stack("unchanged", "- Greetings Consize", filePath), result=Stack("unchanged"))
        content = ""
        with open(filePath, "r") as file:
            content = file.read()
        self.assertEqual(content, "Hello You!\n- Greetings Consize")

    def test_uncomment(self):
        self.__test(cs=Stack("uncomment"), ds=Stack("unchange", "This line % has a comment"), result=Stack("unchanged", "This line"))

    def test_tokenize(self):
        self.__test(
            cs=Stack("tokenize"),
            ds=Stack("unchanged", "This line % has a comment"),
            result=Stack("unchanged", Stack("This","line","%","has","a","comment")))
