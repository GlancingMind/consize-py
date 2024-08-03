from ExternalWords import ExternalWord
from Interpreter import Interpreter

class Word(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[0] != "word":
            return False

        if i.ds == []:
            return False

        wordstack, *rest = i.ds
        i.ds = ["".join(wordstack)] + rest
        return True

class Unword(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[0] != "unword":
            return False

        if i.ds == []:
            return False

        word, *rest = i.ds
        i.ds = [[character for character in word]] + rest
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

        characterCode, *rest = i.ds
        match characterCode:
            case r"\space":     i.ds = [" "] + rest
            case r"\newline":   i.ds = ["\n"] + rest
            case r"\formfeed":  i.ds = ["\f"] + rest
            case r"\return":    i.ds = ["\r"] + rest
            case r"\backspace": i.ds = ["\b"] + rest
            case r"\tab":       i.ds = ["\t"] + rest
            case _ if characterCode.startswith(r"\o"):
                i.ds = [chr(int(characterCode[2:], 8))] + rest
            case _ if characterCode.startswith(r"\u"):
                i.ds = [bytes(characterCode, "utf-8").decode("unicode_escape")] + rest
            case _:
                i.ds = [fr"error: {characterCode} isn't a valid character codec"] + rest
        i.cs.pop()
        return True
