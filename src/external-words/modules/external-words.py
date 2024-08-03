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
