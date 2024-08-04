from ExternalWords import ExternalWord
from Interpreter import Interpreter
from Stack import Stack
from unittest import mock

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
        i.ds = Stack(*rest, "".join(wordstack))
        i.cs.pop()
        return True

class Unword(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "unword":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        i.ds = Stack(*rest, [character for character in word])
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
            case r"\space":     i.ds = Stack(*rest, " ")
            case r"\newline":   i.ds = Stack(*rest, "\n")
            case r"\formfeed":  i.ds = Stack(*rest, "\f")
            case r"\return":    i.ds = Stack(*rest, "\r")
            case r"\backspace": i.ds = Stack(*rest, "\b")
            case r"\tab":       i.ds = Stack(*rest, "\t")
            case _ if characterCode.startswith(r"\o"):
                i.ds = Stack(*rest, chr(int(characterCode[2:], 8)))
            case _ if characterCode.startswith(r"\u"):
                i.ds = Stack(*rest, bytes(characterCode, "utf-8").decode("unicode_escape"))
            case _:
                i.ds = Stack(*rest, fr"error: {characterCode} isn't a valid character codec")
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

        i.ds = Stack(*rest)
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

        i.ds = Stack(*rest, content)
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

        i.ds = Stack(*rest)
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

        i.ds = Stack(*rest)
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
        i.ds = Stack(*rest, *[re.sub(r"(?m)\s*%.*$", "", word).strip()])
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
        i.ds = Stack(*rest, Stack() if parts == [""] else Stack(*parts))
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

        i.ds = Stack(*rest, Stack(r"\r\n".join(parts)))
        i.cs.pop()
        return True

class CurrentTimeMilliSec(ExternalWord):
    def execute(i: Interpreter):
        import time

        if i.cs == [] or i.cs[-1] != "current-time-millis":
            return False

        i.ds.append(int(time.time() * 1000))
        i.cs.pop()
        return True

class OperatingSystem(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs[-1] != "operating-system":
            return False

        import platform
        i.ds.append(platform.platform())
        i.cs.pop()
        return True

class IsInteger(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, num = i.ds
        except ValueError:
            return False

        if cw != "integer?":
            return False

        try:
            result = int(num)
        except (ValueError, TypeError):
            result = "f"

        result = "t" if result != "f" else "f"

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Addition(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != "+":
                return False

            result = int(x)+int(y)
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Subtraction(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != "-":
                return False

            result = int(x)-int(y)
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Multiplication(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != "*":
                return False

            result = int(x)*int(y)
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Devision(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != "div":
                return False

            result = int(x)//int(y)
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Modulus(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != "mod":
                return False

            result = int(x)%int(y)
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class LessThan(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != "<":
                return False

            result = int(x) < int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class MoreThan(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != ">":
                return False

            result = int(x) > int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class MoreThanEqual(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != ">=":
                return False

            result = int(x) >= int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class LessThanEqual(ExternalWord):
    def execute(i: Interpreter):
        try:
            *rcs, cw = i.cs
            *rds, x, y = i.ds

            if cw != "<=":
                return False

            result = int(x) <= int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True
