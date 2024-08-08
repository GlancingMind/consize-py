from Interpreter import Interpreter
from Rule import NativeRule
from Stack import Stack

class Word(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "word":
            return False

        if i.ds == []:
            return False

        *rest, wordstack = i.ds
        i.ds = Stack(*rest, "".join(wordstack))
        i.cs.pop(0)
        return True

class Unword(NativeRule):
    def execute(i: Interpreter):
        if i.cs == [] or i.cs.peek() != "unword":
            return False

        if i.ds == []:
            return False

        *rest, word = i.ds
        i.ds = Stack(*rest, [character for character in word])
        i.cs.pop(0)
        return True

class Char(NativeRule):
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

class Print(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rest, word = i.ds
        except ValueError:
            return False

        if cw != "print":
            return False

        if not isinstance(word, str):
            return False

        print(word, end="")

        i.ds = Stack(*rest)
        i.cs = Stack(*rcs)
        return True

class Flush(NativeRule):
    def execute(i: Interpreter):
        import sys

        if i.cs == [] or i.cs.peek() != "flush":
            return False

        sys.stdout.flush()

        i.cs.pop(0)
        return True

class Readline(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
        except ValueError:
            return False

        if cw != "read-line":
            return False

        i.ds = Stack(*i.ds, input())
        i.cs = Stack(*rcs)
        return True

class Slurp(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rest, source = i.ds
        except ValueError:
            return False

        if cw != "slurp":
            return False

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
        i.cs = Stack(*rcs)
        return True

class Spit(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rest, data, uri = i.ds
        except ValueError:
            return False

        if cw != "spit":
            return False

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
        i.cs = Stack(*rcs)
        return True

class SpitOn(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rest, data, uri = i.ds
        except ValueError:
            return False

        if cw != "spit-on":
            return False

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
        i.cs = Stack(*rcs)
        return True

class Uncomment(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rest, word = i.ds
        except ValueError:
            return False

        if cw != "uncomment":
            return False

        import re
        i.ds = Stack(*rest, *[re.sub(r"(?m)\s*%.*$", "", word).strip()])
        i.cs = Stack(*rcs)
        return True

class Tokenize(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rest, word = i.ds
        except ValueError:
            return False

        if cw != "tokenize":
            return False

        import re
        parts = re.split(r"\s+", word.strip())
        i.ds = Stack(*rest, Stack() if parts == [""] else Stack(*parts))
        i.cs = Stack(*rcs)
        return True

class Undocument(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rest, word = i.ds
        except ValueError:
            return False

        if cw != "undocument":
            return False

        import re
        parts = re.findall(r"(?m)^%?>> (.*)$", word)
        i.ds = Stack(*rest, Stack(r"\r\n".join(parts)))
        i.cs = Stack(*rcs)
        return True

class CurrentTimeMilliSec(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
        except ValueError:
            return False

        if cw != "current-time-millis":
            return False

        import time
        i.ds = Stack(*i.ds, int(time.time() * 1000))
        i.cs = Stack(*rcs)
        return True

class OperatingSystem(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
        except ValueError:
            return False

        if cw != "operating-system":
            return False

        import platform

        i.cs = Stack(*rcs)
        i.ds = Stack(*i.ds, platform.platform())
        return True

class IsInteger(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
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

class Addition(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rds, x, y = i.ds

            if cw != "+":
                return False

            result = str(int(x)+int(y))
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Subtraction(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rds, x, y = i.ds

            if cw != "-":
                return False

            result = str(int(x)-int(y))
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Multiplication(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rds, x, y = i.ds

            if cw != "*":
                return False

            result = str(int(x)*int(y))
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Devision(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rds, x, y = i.ds

            if cw != "div":
                return False

            result = str(int(x)//int(y))
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class Modulus(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
            *rds, x, y = i.ds

            if cw != "mod":
                return False

            result = str(int(x)%int(y))
        except (ValueError, TypeError):
            return False

        i.cs = Stack(*rcs)
        i.ds = Stack(*rds, result)
        return True

class LessThan(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
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

class MoreThan(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
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

class MoreThanEqual(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
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

class LessThanEqual(NativeRule):
    def execute(i: Interpreter):
        try:
            cw, *rcs = i.cs
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
