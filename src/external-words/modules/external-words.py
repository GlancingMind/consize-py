from ExternalWords import ExternalWord
from Interpreter import Interpreter

# TODO move call- and datastack validation into superclass.
# The just call super.match(), or let ExternalWords.py call isSatisfied() and
# only when this is True, then ExternalWords will call execute. This way the
# check cannot be forgotten.

class Word(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[0] != "word":
            return False

        if i.ds == []:
            return False

        *rest, wordstack = i.ds
        i.ds = rest + ["".join(wordstack)]
        i.cs.pop()
        return True

class Unword(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[0] != "unword":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        i.ds = rest + [[character for character in word]]
        i.cs.pop()
        return True

class Char(ExternalWord):
    def execute(i: Interpreter):
        """
        :return: New stack with the top most element being the interpreted
        character.

        NOTE: Top element on the stack should be a raw string, otherwise
        interpretation will fail.

        E.g: char([r"\\u0040"]) will return ["@"]
            char([r"\\o100"]) will return ["@"]
        """
        if i.cs == [] or i.cs[0] != "char":
            return False

        if i.ds == []:
            return False

        *rest, characterCode = i.ds
        match characterCode:
            case r"\space":     i.ds = rest + [" "]
            case r"\newline":   i.ds = rest + ["\n"]
            case r"\formfeed":  i.ds = rest + ["\f"]
            case r"\return":    i.ds = rest + ["\r"]
            case r"\backspace": i.ds = rest + ["\b"]
            case r"\tab":       i.ds = rest + ["\t"]
            case _ if characterCode.startswith(r"\o"):
                i.ds = rest + [chr(int(characterCode[2:], 8))]
            case _ if characterCode.startswith(r"\u"):
                i.ds = rest + [bytes(characterCode, "utf-8").decode("unicode_escape")]
            case _:
                i.ds = rest + [fr"error: {characterCode} isn't a valid character codec"]
        i.cs.pop()
        return True

class Print(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[0] != "print":
            return False

        if i.ds == []:
            return False

        word, *rest = i.ds
        if not isinstance(word, str):
            return False

        print(word, end="")

        i.ds = rest
        i.cs.pop()
        return True

class Flush(ExternalWord):
    def execute(i: Interpreter):
        import sys

        if i.cs == [] or i.cs[0] != "flush":
            return False

        sys.stdout.flush()

        i.cs.pop()
        return True

class Readline(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[0] != "read-line":
            return False

        i.ds.append(input())
        i.cs.pop()
        return True
