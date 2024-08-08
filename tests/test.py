import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from io import StringIO
import unittest
from unittest import mock

from Interpreter import Interpreter
from Stack import Dictionary, Stack

class Test(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        i = Interpreter(native_rule_module_dir="external-words")
        i.replace_ruleset("consize.ruleset")
        self.consize_ruleset = i.ruleset
        self.native_rules = i.native_rules

    def __test(self, ds, cs, result_ds, result_cs=None):
        i = Interpreter(ruleset=self.consize_ruleset, cs=cs, ds=ds)
        i.native_rules = self.native_rules
        i.run(interactive=False)
        self.assertEqual(i.ds, result_ds)
        if result_cs:
            self.assertEqual(i.cs, result_cs)

    def test_swap(self):
        self.__test(cs=Stack("swap"), ds=Stack("1","2","2","3"), result_ds=Stack("1","2","3","2"))

    def test_dup(self):
        self.__test(cs=Stack("dup"), ds=Stack("1","2","2","3"), result_ds=Stack("1","2","2","3","3"))

    def test_drop(self):
        self.__test(cs=Stack("drop"), ds=Stack("1","2","3"), result_ds=Stack("1","2"))

    def test_rot(self):
        self.__test(cs=Stack("rot"), ds=Stack("1","2","3","4"), result_ds=Stack("1","4","2","3"))

    def test_equal(self):
        self.__test(cs=Stack("equal?"), ds=Stack("1","1"), result_ds=Stack("t"))
        self.__test(cs=Stack("equal?"), ds=Stack("1","2"), result_ds=Stack("f"))
        self.__test(cs=Stack("equal?"), ds=Stack("1","2","2"), result_ds=Stack("1","t"))
        self.__test(cs=Stack("equal?"), ds=Stack("1","2","3"), result_ds=Stack("1","f"))

    def test_identical(self):
        self.__test(cs=Stack("identical?"), ds=Stack("1","1"), result_ds=Stack("t"))
        self.__test(cs=Stack("identical?"), ds=Stack("1","2"), result_ds=Stack("f"))
        self.__test(cs=Stack("identical?"), ds=Stack("1","2","2"), result_ds=Stack("1","t"))
        self.__test(cs=Stack("identical?"), ds=Stack("1","2","3"), result_ds=Stack("1","f"))

    def test_emptystack(self):
        self.__test(cs=Stack("emptystack"), ds=Stack(), result_ds=Stack(Stack()))
        self.__test(cs=Stack("emptystack"), ds=Stack("1","2"), result_ds=Stack("1","2",Stack()))

    def test_push(self):
        self.__test(cs=Stack("push"), ds=Stack("1","2","2",Stack("4","3"),"5"), result_ds=Stack("1","2","2",Stack("5","4","3")))

    def test_top(self):
        # self.__test(cs=Stack("top"), ds=Stack("1","2","2","3","nil"), result_ds=Stack("1","2","2","3","nil"))
        self.__test(cs=Stack("top"), ds=Stack("1","2","2","3",Stack()), result_ds=Stack("1","2","2","3","nil"))
        # self.__test(cs=Stack("top"), ds=Stack("1","2","2","3",Stack("a")), result_ds=Stack("1","2","2","3","a"))
        # self.__test(cs=Stack("top"), ds=Stack("1","2","2","3",Stack("a","b")), result_ds=Stack("1","2","2","3","a"))

    def test_pop(self):
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack()), result_ds=Stack("1","2","2","3",Stack()))
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack("a")), result_ds=Stack("1","2","2","3",Stack()))
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack("a","b")), result_ds=Stack("1","2","2","3",Stack("b")))
        self.__test(cs=Stack("pop"), ds=Stack("1","2","2","3",Stack("a","b","c")), result_ds=Stack("1","2","2","3",Stack("b","c")))

    def test_unpush(self):
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack()), result_ds=Stack("1","2",Stack(), "nil"))
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack("a")), result_ds=Stack("1","2",Stack(),"a"))
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack("a","b")), result_ds=Stack("1","2",Stack("b"),"a"))
        self.__test(cs=Stack("unpush"), ds=Stack("1","2",Stack("a", "b", "c")), result_ds=Stack("1","2",Stack("b", "c"),"a"))

    def test_concat(self):
        # self.__test(cs=Stack("concat"), ds=Stack(Stack(),Stack()), result_ds=Stack(Stack()))
        # self.__test(cs=Stack("concat"), ds=Stack(Stack("a"),Stack("b")), result_ds=Stack(Stack("a","b")))
        self.__test(cs=Stack("concat"), ds=Stack(Stack("a","b"), Stack("c","d")), result_ds=Stack(Stack("a","b","c","d")))

    def test_escape(self):
        self.__test(cs=Stack("\\", "a"), ds=Stack(), result_ds=Stack("a"))
        self.__test(cs=Stack("\\", "a"), ds=Stack(Stack()), result_ds=Stack(Stack(), "a"))
        self.__test(cs=Stack("\\", "a"), ds=Stack("unchanged"), result_ds=Stack("unchanged", "a"))

    def test_reverse(self):
        self.__test(cs=Stack("reverse"), ds=Stack(Stack()), result_ds=Stack(Stack()))
        self.__test(cs=Stack("reverse"), ds=Stack(Stack("1")), result_ds=Stack(Stack("1")))
        self.__test(cs=Stack("reverse"), ds=Stack(Stack("1","2")), result_ds=Stack(Stack("2","1")))
        self.__test(cs=Stack("reverse"), ds=Stack(Stack("1",Stack("2","3"),"4")), result_ds=Stack(Stack("4",Stack("2","3"),"1")))

    def test_mapping(self):
        self.__test(cs=Stack("mapping"), ds=Stack(Stack()), result_ds=Stack(Dictionary()))
        self.__test(cs=Stack("mapping"), ds=Stack(Stack("a","1")), result_ds=Stack(Dictionary("a","1")))
        self.__test(cs=Stack("mapping"), ds=Stack(Stack("a","1","b","2")), result_ds=Stack(Dictionary("a","1","b","2")))
        self.__test(cs=Stack("mapping"), ds=Stack("unchanged", Stack("a","1","b","2")), result_ds=Stack("unchanged", Dictionary("a","1","b","2")))

    def test_unmap(self):
        self.__test(cs=Stack("unmap"), ds=Stack(Dictionary()), result_ds=Stack(Stack()))
        self.__test(cs=Stack("unmap"), ds=Stack(Dictionary("a","1")), result_ds=Stack(Stack("a","1")))
        self.__test(cs=Stack("unmap"), ds=Stack(Dictionary("a","1", "b","2")), result_ds=Stack(Stack("a","1","b","2")))
        self.__test(cs=Stack("unmap"), ds=Stack("unchanged", Dictionary("a","1", "b","2")), result_ds=Stack("unchanged", Stack("a","1","b","2")))

    def test_keys(self):
        self.__test(cs=Stack("keys"), ds=Stack("unchanged", Dictionary()), result_ds=Stack("unchanged", Stack()))
        self.__test(cs=Stack("keys"), ds=Stack("unchanged", Dictionary("a","1")), result_ds=Stack("unchanged", Stack("a")))
        self.__test(cs=Stack("keys"), ds=Stack("unchanged", Dictionary("a","1", "b","2")), result_ds=Stack("unchanged", Stack("a","b")))

    def test_assoc(self):
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "v", "k", Dictionary()), result_ds=Stack("unchanged", Dictionary("k", "v")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "v", "k", Dictionary("k", "v")), result_ds=Stack("unchanged", Dictionary("k", "v")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "b", "k", Dictionary("k", "v")), result_ds=Stack("unchanged", Dictionary("k", "b")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "v2", "k2", Dictionary("k", "v")), result_ds=Stack("unchanged", Dictionary("k", "v", "k2", "v2")))
        self.__test(cs=Stack("assoc"), ds=Stack("unchanged", "changed", "k", Dictionary("x","z","k","b","a","v")), result_ds=Stack("unchanged", Dictionary("x","z","a","v","k","changed")))

    def test_dissoc(self):
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "k", Dictionary()), result_ds=Stack("unchanged", Dictionary()))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "k", Dictionary("k", "v")), result_ds=Stack("unchanged", Dictionary()))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "x", Dictionary("x","z","k","b","a","v")), result_ds=Stack("unchanged", Dictionary("k","b","a","v")))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "k", Dictionary("x","z","k","b","a","v")), result_ds=Stack("unchanged", Dictionary("x","z","a","v")))
        self.__test(cs=Stack("dissoc"), ds=Stack("unchanged", "a", Dictionary("x","z","k","b","a","v")), result_ds=Stack("unchanged", Dictionary("x","z","k","b")))

    def test_get(self):
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary(), "d"), result_ds=Stack("unchanged", "d"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("a","b"), "d"), result_ds=Stack("unchanged", "d"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("a","b","c","e"), "d"), result_ds=Stack("unchanged", "d"))

        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("k","v"), "d"), result_ds=Stack("unchanged", "v"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("a","v","k","b"), "d"), result_ds=Stack("unchanged", "b"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("k","b","a","v"), "d"), result_ds=Stack("unchanged", "b"))
        self.__test(cs=Stack("get"), ds=Stack("unchanged", "k", Dictionary("x","z","k","b","a","v"), "d"), result_ds=Stack("unchanged", "b"))

    def test_merge(self):
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary(), Dictionary()), result_ds=Stack("unchanged", Dictionary()))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary(), Dictionary("k", "v")), result_ds=Stack("unchanged", Dictionary("k","v")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("k", "v"), Dictionary()), result_ds=Stack("unchanged", Dictionary("k","v")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("x","z","k","b"), Dictionary("a","v")), result_ds=Stack("unchanged", Dictionary("x","z", "k","b", "a","v")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("x","z"), Dictionary("k","b","a","v")), result_ds=Stack("unchanged", Dictionary("x","z", "a","v", "k","b")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("a","z", "k","b", "e","x"), Dictionary("a","changed",)), result_ds=Stack("unchanged", Dictionary("k","b", "e","x", "a","changed")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("a","z", "k","b", "e","x"), Dictionary("k","changed",)), result_ds=Stack("unchanged", Dictionary("a","z", "e","x", "k","changed")))
        self.__test(cs=Stack("merge"), ds=Stack("unchanged", Dictionary("a","z", "k","b", "e","x"), Dictionary("e","changed",)), result_ds=Stack("unchanged", Dictionary("a","z", "k","b", "e","changed")))

    def test_unword(self):
        self.__test(cs=Stack("unword"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("unword"), ds=Stack("unchanged", "Hello"), result_ds=Stack("unchanged", Stack("H","e","l","l","o")))

    def test_word(self):
        self.__test(cs=Stack("word"), ds=Stack(Stack("1")), result_ds=Stack("1"))
        self.__test(cs=Stack("word"), ds=Stack("unchanged", Stack("1","2")), result_ds=Stack("unchanged", "12"))

    def test_char(self):
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\space"), result_ds=Stack("unchanged", " "))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\newline"), result_ds=Stack("unchanged", "\n"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\formfeed"), result_ds=Stack("unchanged","\f"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\return"), result_ds=Stack("unchanged","\r"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\backspace"), result_ds=Stack("unchanged","\b"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\tab"), result_ds=Stack("unchanged","\t"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\u0040"), result_ds=Stack("unchanged","@"))
        self.__test(cs=Stack("char"), ds=Stack("unchanged", r"\o100"), result_ds=Stack("unchanged","@"))

    def test_print(self):
        self.__test(cs=Stack("print"), ds=Stack("Hello World"), result_ds=Stack())

    def test_readline(self):
        from contextlib import contextmanager

        @contextmanager
        def replace_stdin(target):
            orig = sys.stdin
            sys.stdin = target
            yield
            sys.stdin = orig
        with replace_stdin(StringIO("Some preprogrammed input")):
            self.__test(cs=Stack("read-line"), ds=Stack(), result_ds=Stack("Some preprogrammed input"))

    def test_slurp(self):
        self.__test(cs=Stack("slurp"), ds=Stack("./tests/test-file-for-slurp.txt"), result_ds=Stack("Hello Consize!\n"))

    def test_spit(self):
        filePath = "./tests/test-file-for-spit.txt"
        with open(filePath, "w") as file:
            file.write("")
        self.__test(cs=Stack("spit"), ds=Stack("unchanged", "Hello Consize!\n", filePath), result_ds=Stack("unchanged"))
        content = ""
        with open(filePath, "r") as file:
            content = file.read()
        self.assertEqual(content, "Hello Consize!\n")

    def test_spit_on(self):
        filePath = "./tests/test-file-for-spit-on.txt"
        data = "Hello You!\n"
        with open(filePath, "w") as file:
            file.write(data)
        self.__test(cs=Stack("spit-on"), ds=Stack("unchanged", "- Greetings Consize", filePath), result_ds=Stack("unchanged"))
        content = ""
        with open(filePath, "r") as file:
            content = file.read()
        self.assertEqual(content, "Hello You!\n- Greetings Consize")

    def test_uncomment(self):
        self.__test(cs=Stack("uncomment"), ds=Stack("unchanged", "This line % has a comment"), result_ds=Stack("unchanged", "This line"))

    def test_tokenize(self):
        self.__test(
            cs=Stack("tokenize"),
            ds=Stack("unchanged", "This line % has a comment"),
            result_ds=Stack("unchanged", Stack("This","line","%","has","a","comment")))

    def test_undocument(self):
        self.__test(
            cs=Stack("undocument"),
            ds=Stack("unchanged", "Some documentation is nice.\n>> dup rot rot\nWhat might this do? Here is some other code\n%>> swap"),
            result_ds=Stack("unchanged", Stack(r"dup rot rot\r\nswap")))

    @mock.patch('time.time', mock.MagicMock(return_value=42))
    def test_current_time_millis(self):
        self.__test(cs=Stack("current-time-millis"), ds=Stack("unchanged"), result_ds=Stack("unchanged", 42000))

    @mock.patch('platform.platform', mock.MagicMock(return_value="macOS-14.6-arm64-arm-64bit"))
    def test_operating_system(self):
        self.__test(cs=Stack("operating-system"), ds=Stack("unchanged"), result_ds=Stack("unchanged", "macOS-14.6-arm64-arm-64bit"))

    def test_integer(self):
        self.__test(cs=Stack("integer?"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("integer?"), ds=Stack("a"), result_ds=Stack("f"))
        self.__test(cs=Stack("integer?"), ds=Stack("unchanged", 7), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack("integer?"), ds=Stack("unchanged", "7"), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack("integer?"), ds=Stack("unchanged", "-7"), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack("integer?"), ds=Stack("unchanged", -7), result_ds=Stack("unchanged", "t"))

    def test_plus(self):
        self.__test(cs=Stack("+"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("+"), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack("+"), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack("+"), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "0"))
        self.__test(cs=Stack("+"), ds=Stack("unchanged", "1", "7", "7"), result_ds=Stack("unchanged", "1", "14"))
        self.__test(cs=Stack("+"), ds=Stack("unchanged", "1", 7, "7"), result_ds=Stack("unchanged", "1", "14"))
        self.__test(cs=Stack("+"), ds=Stack("unchanged", "1", "7", 7), result_ds=Stack("unchanged", "1", "14"))

    def test_minus(self):
        self.__test(cs=Stack("-"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("-"), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack("-"), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack("-"), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "-14"))
        self.__test(cs=Stack("-"), ds=Stack("unchanged", "1", "7", "7"), result_ds=Stack("unchanged", "1", "0"))
        self.__test(cs=Stack("-"), ds=Stack("unchanged", "1", 7, "7"), result_ds=Stack("unchanged", "1", "0"))
        self.__test(cs=Stack("-"), ds=Stack("unchanged", "1", "7", 7), result_ds=Stack("unchanged", "1", "0"))

    def test_multiply(self):
        self.__test(cs=Stack("*"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("*"), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack("*"), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack("*"), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "-49"))
        self.__test(cs=Stack("*"), ds=Stack("unchanged", "1", "7", "7"), result_ds=Stack("unchanged", "1", "49"))
        self.__test(cs=Stack("*"), ds=Stack("unchanged", "1", 7, "7"), result_ds=Stack("unchanged", "1", "49"))
        self.__test(cs=Stack("*"), ds=Stack("unchanged", "1", "7", 7), result_ds=Stack("unchanged", "1", "49"))

    def test_div(self):
        self.__test(cs=Stack("div"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("div"), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack("div"), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack("div"), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "-1"))
        self.__test(cs=Stack("div"), ds=Stack("unchanged", "1", "7", "7"), result_ds=Stack("unchanged", "1", "1"))
        self.__test(cs=Stack("div"), ds=Stack("unchanged", "1", 7, "7"), result_ds=Stack("unchanged", "1", "1"))
        self.__test(cs=Stack("div"), ds=Stack("unchanged", "1", "7", 7), result_ds=Stack("unchanged", "1", "1"))

    def test_lessthan(self):
        self.__test(cs=Stack("<"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("<"), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack("<"), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", 1, "-7", "7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", 1, -7, "7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", 1, "-7", 7), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", 7, 7), result_ds=Stack("unchanged", "f"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", 1, "7", "7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", 1, 7, "7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack("<"), ds=Stack("unchanged", 1, "7", 7), result_ds=Stack("unchanged", 1, "f"))

    def test_lessthanequal(self):
        self.__test(cs=Stack("<="), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack("<="), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack("<="), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, "-7", "7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, -7, "7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, "-7", 7), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 7, 7), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, "7", "7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, 7, "7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, "7", "-7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, 7, "-7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack("<="), ds=Stack("unchanged", 1, 7, "-7"), result_ds=Stack("unchanged", 1, "f"))

    def test_morethan(self):
        self.__test(cs=Stack(">"), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack(">"), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack(">"), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "f"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", 1, "-7", "7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", 1, -7, "7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", 1, "-7", 7), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", 7, -7), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", 1, "7", "-7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", 1, 7, "-7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack(">"), ds=Stack("unchanged", 1, "7", -7), result_ds=Stack("unchanged", 1, "t"))

    def test_morethanequal(self):
        self.__test(cs=Stack(">="), ds=Stack(), result_ds=Stack())
        self.__test(cs=Stack(">="), ds=Stack("a"), result_ds=Stack("a"))
        self.__test(cs=Stack(">="), ds=Stack("a","b"), result_ds=Stack("a","b"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", -7, 7), result_ds=Stack("unchanged", "f"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 1, "-7", "7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 1, -7, "7"), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 1, "-7", 7), result_ds=Stack("unchanged", 1, "f"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 7, -7), result_ds=Stack("unchanged", "t"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 1, "7", "-7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 1, 7, "-7"), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 1, "7", -7), result_ds=Stack("unchanged", 1, "t"))
        self.__test(cs=Stack(">="), ds=Stack("unchanged", 1, "7", 7), result_ds=Stack("unchanged", 1, "t"))

    def test_callcc(self):
        # We cannot use a valid word within the quotation, otherwise the
        # matching-system will try to apply this word too, resulting in a
        # changed datastack. Therefore we will use `blub` as word, which isn't
        # part of the Consize-RuleSet and cannot be substituded further.
        # Therefore the system will stop after call/cc.
        self.__test(
            cs=Stack("call/cc","RCS"),
            ds=Stack("RDS", Stack("blub")),
            result_ds=Stack(Stack("RDS"), Stack("RCS")),
            result_cs=Stack("blub"))

    def test_continue(self):
        self.__test(
            cs=Stack("continue","RCS"),
            ds=Stack("RDS", Stack("NDS","NDS_REST"), Stack("NCS","NCS_REST")),
            result_ds=Stack("NDS","NDS_REST"),
            result_cs=Stack("NCS","NCS_REST"))

    def test_call(self):
        self.__test(cs=Stack("call"), ds=Stack("unchanged", "1", Stack("integer?")), result_ds=Stack("unchanged", "t"))

    def test_clear(self):
        self.__test(cs=Stack("clear","RCS"), ds=Stack("1","2","3"), result_ds=Stack(), result_cs=Stack("RCS"))

    def test_size(self):
        self.__test(cs=Stack("size"), ds=Stack(Stack()), result_ds=Stack("0"))
        self.__test(cs=Stack("size"), ds=Stack(Stack("a")), result_ds=Stack("1"))
        self.__test(cs=Stack("size"), ds=Stack(Stack("a","b")), result_ds=Stack("2"))

    def test_sum(self):
        self.__test(cs=Stack("sum"), ds=Stack(Stack()), result_ds=Stack("0"))
        self.__test(cs=Stack("sum"), ds=Stack(Stack("2")), result_ds=Stack("2"))
        self.__test(cs=Stack("sum"), ds=Stack(Stack("1","2")), result_ds=Stack("3"))
        self.__test(cs=Stack("sum"), ds=Stack(Stack("1","2","3","4")), result_ds=Stack("10"))

    def test_my_size(self):
        self.__test(cs=Stack("my-size"), ds=Stack(Stack()), result_ds=Stack("0"))
        self.__test(cs=Stack("my-size"), ds=Stack(Stack("2")), result_ds=Stack("1"))
        self.__test(cs=Stack("my-size"), ds=Stack(Stack("1","2")), result_ds=Stack("2"))
        self.__test(cs=Stack("my-size"), ds=Stack(Stack("1","2","3","4")), result_ds=Stack("4"))

    def test_my_reverse(self):
        self.__test(cs=Stack("my-reverse"), ds=Stack(Stack()), result_ds=Stack(Stack()))
        self.__test(cs=Stack("my-reverse"), ds=Stack(Stack("2")), result_ds=Stack(Stack("2")))
        self.__test(cs=Stack("my-reverse"), ds=Stack(Stack("1","2")), result_ds=Stack(Stack("2","1")))
        self.__test(cs=Stack("my-reverse"), ds=Stack(Stack("2","1")), result_ds=Stack(Stack("1","2")))
        self.__test(cs=Stack("my-reverse"), ds=Stack(Stack("1","2","3","4")), result_ds=Stack(Stack("4","3","2","1")))
