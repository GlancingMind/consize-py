from CommandLoader import ExternalWord
from Interpreter import Interpreter
from Rule import Rule
import RuleParser
from Stack import Stack
from StackPattern import StackPattern
import StackPattern

# TODO move call- and datastack validation into superclass.
# The just call super.match(), or let ExternalWords.py call isSatisfied() and
# only when this is True, then ExternalWords will call execute. This way the
# check cannot be forgotten.
# TODO add name attribute to ExternalWord, so that ExternalWordLoader can print
# the Word from rule

# class AddToRuleSet(ExternalWord):
#     def execute(i: Interpreter):
#         # TODO if a word is unkown, call read-word, which will move the word
#         # over to the datastack
#         rule = RuleParser.parse(" | ; -> ")
#         matches = rule.matches(i)
#         if not matches:
#             return False

#         rule = matches["@RULE"]
#         i.add_rule1(rule)

#         *rest, wordstack = i.ds
#         i.ds = StackPattern
#         i.cs.pop(0)
#         return True

class Word(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "word":
            return False

        if i.ds == []:
            return False

        *rest, wordstack = i.ds
        i.ds = Stack(*rest, "".join(wordstack))
        i.cs.pop(0)
        return True

class Unword(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "unword":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        i.ds = Stack(*rest, [character for character in word])
        i.cs.pop(0)
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
        if i.cs == [] or i.cs.peek() != "char":
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
        i.cs.pop(0)
        return True

class Print(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "print":
            return False

        if i.ds == []:
            return False

        word, *rest = i.ds
        if not isinstance(word, str):
            return False

        print(word, end="")

        i.ds = Stack(*rest)
        i.cs.pop(0)
        return True

class Flush(ExternalWord):
    def execute(i: Interpreter):
        import sys

        if i.cs == [] or i.cs.peek() != "flush":
            return False

        sys.stdout.flush()

        i.cs.pop(0)
        return True

class Readline(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "read-line":
            return False

        i.ds.append(input())
        i.cs.pop(0)
        return True

class Slurp(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "slurp":
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
        i.cs.pop(0)
        return True

class Spit(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "spit":
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
        i.cs.pop(0)
        return True

class SpitOn(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "spit-on":
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
        i.cs.pop(0)
        return True

class Uncomment(ExternalWord):
    def execute(i: Interpreter):
        import re

        if i.cs == [] or i.cs.peek() != "uncomment":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        i.ds = Stack(*rest, *[re.sub(r"(?m)\s*%.*$", "", word).strip()])
        i.cs.pop(0)
        return True

class Tokenize(ExternalWord):
    def execute(i: Interpreter):
        import re

        if i.cs == [] or i.cs.peek() != "tokenize":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        parts = re.split(r"\s+", word.strip())
        i.ds = Stack(*rest, Stack() if parts == [""] else Stack(*parts))
        i.cs.pop(0)
        return True

class Undocument(ExternalWord):
    def execute(i: Interpreter):
        import re

        if i.cs == [] or i.cs.peek() != "undocument":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        parts = re.findall(r"(?m)^%?>> (.*)$", word)

        i.ds = Stack(*rest, Stack(r"\r\n".join(parts)))
        i.cs.pop(0)
        return True

class CurrentTimeMilliSec(ExternalWord):
    def execute(i: Interpreter):
        import time

        if i.cs == [] or i.cs.peek() != "current-time-millis":
            return False

        i.ds.append(int(time.time() * 1000))
        i.cs.pop(0)
        return True

class OperatingSystem(ExternalWord):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "operating-system":
            return False

        import platform
        i.ds.append(platform.platform())
        i.cs.pop(0)
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

# class Reverse(ExternalWord):
#     def execute(i: Interpreter):

#         if i.cs == [] or i.cs.peek() != "reverse":
#             return False

#         if i.ds == []:
#             return False

#         *rest, word = i.ds
#         word.reverse()
#         i.ds = Stack(*rest, word)
#         i.cs.pop(0)
#         return True
