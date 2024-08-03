from ExternalWords import ExternalWord
from Interpreter import Interpreter
from Stack import Stack

# TODO move call- and datastack validation into superclass.
# The just call super.match(), or let ExternalWords.py call isSatisfied() and
# only when this is True, then ExternalWords will call execute. This way the
# check cannot be forgotten.

class Word(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "word":
            return False

        if i.ds == []:
            return False

        *rest, wordstack = i.ds
        i.ds = rest + ["".join(wordstack)]
        i.cs.pop()
        return True

class Unword(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "unword":
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
        if i.cs == [] or i.cs[-1] != "char":
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
        if i.cs == [] or i.cs[-1] != "print":
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

        if i.cs == [] or i.cs[-1] != "flush":
            return False

        sys.stdout.flush()

        i.cs.pop()
        return True

class Readline(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "read-line":
            return False

        i.ds.append(input())
        i.cs.pop()
        return True

class Slurp(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "slurp":
            return False

        if i.ds == []:
            return False

        *rest, source = i.ds

        # TODO reading of remote files isn't implemented, to reduce dependencies
        # to request library.
        content = ""
        try:
            with open(source, "r") as file:
                content = file.read()
        except FileNotFoundError:
            print("File not found:", source)
        except PermissionError:
            print("Permission denied to read file:", source)
        except IOError as e:
            print("An error occurred while reading the file:", e)

        i.ds = rest + [content]
        i.cs.pop()
        return True

class Spit(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "spit":
            return False

        if i.ds == []:
            return False

        *rest, data, uri = i.ds

        # seems to be not a valid URI. Will use local file read.
        try:
            with open(uri, "w") as file:
                file.write(data)
        except FileNotFoundError:
            print("File not found:", uri)
        except PermissionError:
            print("Permission denied to write file:", uri)
        except IOError as e:
            print("An error occurred while writing the file:", e)

        i.ds = rest
        i.cs.pop()
        return True

class SpitOn(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "spit-on":
            return False

        if i.ds == []:
            return False

        *rest, data, uri = i.ds

        try:
            with open(uri, "a") as file:
                file.write(data)
        except FileNotFoundError:
            print("File not found:", uri)
        except PermissionError:
            print("Permission denied to write file:", uri)
        except IOError as e:
            print("An error occurred while writing the file:", e)

        i.ds = rest
        i.cs.pop()
        return True

class Uncomment(ExternalWord):
    def execute(i: Interpreter):
        import re

        if i.cs == [] or i.cs[-1] != "uncomment":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        i.ds = rest + [re.sub(r"(?m)\s*%.*$", "", word).strip()]
        i.cs.pop()
        return True

class Tokenize(ExternalWord):
    def execute(i: Interpreter):
        import re

        if i.cs == [] or i.cs[-1] != "tokenize":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        parts = re.split(r"\s+", word.strip())
        i.ds = rest + ([] if parts == [""] else [parts])
        i.cs.pop()
        return True

class Undocument(ExternalWord):
    def execute(i: Interpreter):
        import re

        if i.cs == [] or i.cs[-1] != "undocument":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        parts = re.findall(r"(?m)^%?>> (.*)$", word)

        # TODO the unstructoring creates list. Which results in i.ds being assigned a list, which is not longer a stack!

        i.ds = Stack(*rest, Stack(r"\r\n".join(parts)))
        i.cs.pop()
        return True
