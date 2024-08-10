from Interpreter import Interpreter
from Rule import AliasRule, NativeRule
import RuleParser
from Stack import Stack

class Word(NativeRule):
    def execute(self, interpreter: Interpreter):
        if interpreter.cs == [] or interpreter.cs.peek() != "word":
            return False

        if interpreter.ds == []:
            return False

        *rest, wordstack = interpreter.ds
        interpreter.ds = Stack(*rest, "".join(wordstack))
        interpreter.cs.pop(0)
        return True

class Unword(NativeRule):
    def execute(self, interpreter: Interpreter):
        if interpreter.cs == [] or interpreter.cs.peek() != "unword":
            return False

        if interpreter.ds == []:
            return False

        *rest, word = interpreter.ds
        interpreter.ds = Stack(*rest, [character for character in word])
        interpreter.cs.pop(0)
        return True

class Char(NativeRule):
    def execute(self, interpreter: Interpreter):
        """
        :return: New stack with the top most element being the interpreted
        character.

        NOTE: Top element on the stack should be a raw string, otherwise
        interpretation will fail.

        E.g: char([r"\\u0040"]) will return ["@"]
            char([r"\\o100"]) will return ["@"]
        """
        if interpreter.cs == [] or interpreter.cs.peek() != "char":
            return False

        if interpreter.ds == []:
            return False

        *rest, characterCode = interpreter.ds
        match characterCode:
            case r"\space":     interpreter.ds = Stack(*rest, " ")
            case r"\newline":   interpreter.ds = Stack(*rest, "\n")
            case r"\formfeed":  interpreter.ds = Stack(*rest, "\f")
            case r"\return":    interpreter.ds = Stack(*rest, "\r")
            case r"\backspace": interpreter.ds = Stack(*rest, "\b")
            case r"\tab":       interpreter.ds = Stack(*rest, "\t")
            case _ if characterCode.startswith(r"\o"):
                interpreter.ds = Stack(*rest, chr(int(characterCode[2:], 8)))
            case _ if characterCode.startswith(r"\u"):
                interpreter.ds = Stack(*rest, bytes(characterCode, "utf-8").decode("unicode_escape"))
            case _:
                interpreter.ds = Stack(*rest, fr"error: {characterCode} isn't a valid character codec")
        interpreter.cs.pop(0)
        return True

class Print(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rest, word = interpreter.ds
        except ValueError:
            return False

        if cw != "print":
            return False

        if not isinstance(word, str):
            return False

        print(word, end="")

        interpreter.ds = Stack(*rest)
        interpreter.cs = Stack(*rcs)
        return True

class Flush(NativeRule):
    def execute(self, interpreter: Interpreter):
        import sys

        if interpreter.cs == [] or interpreter.cs.peek() != "flush":
            return False

        sys.stdout.flush()

        interpreter.cs.pop(0)
        return True

class Readline(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
        except ValueError:
            return False

        if cw != "read-line":
            return False

        interpreter.ds = Stack(*interpreter.ds, input())
        interpreter.cs = Stack(*rcs)
        return True

class Slurp(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rest, source = interpreter.ds
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

        interpreter.ds = Stack(*rest, content)
        interpreter.cs = Stack(*rcs)
        return True

class Spit(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rest, data, uri = interpreter.ds
        except ValueError:
            return False

        if cw != "spit":
            return False

        # seems to be not a valid URinterpreter. Will use local file read.
        try:
            with open(uri, "w") as file:
                file.write(data)
        except FileNotFoundError:
            print("File not found:", uri)
        except PermissionError:
            print("Permission denied to write file:", uri)
        except IOError as e:
            print("An error occurred while writing the file:", e)

        interpreter.ds = Stack(*rest)
        interpreter.cs = Stack(*rcs)
        return True

class SpitOn(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rest, data, uri = interpreter.ds
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

        interpreter.ds = Stack(*rest)
        interpreter.cs = Stack(*rcs)
        return True

class Uncomment(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rest, word = interpreter.ds
        except ValueError:
            return False

        if cw != "uncomment":
            return False

        import re
        interpreter.ds = Stack(*rest, *[re.sub(r"(?m)\s*%.*$", "", word).strip()])
        interpreter.cs = Stack(*rcs)
        return True

class Tokenize(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rest, word = interpreter.ds
        except ValueError:
            return False

        if cw != "tokenize":
            return False

        import re
        parts = re.split(r"\s+", word.strip())
        interpreter.ds = Stack(*rest, Stack() if parts == [""] else Stack(*parts))
        interpreter.cs = Stack(*rcs)
        return True

class Undocument(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rest, word = interpreter.ds
        except ValueError:
            return False

        if cw != "undocument":
            return False

        import re
        parts = re.findall(r"(?m)^%?>> (.*)$", word)
        interpreter.ds = Stack(*rest, Stack(r"\r\n".join(parts)))
        interpreter.cs = Stack(*rcs)
        return True

class CurrentTimeMilliSec(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
        except ValueError:
            return False

        if cw != "current-time-millis":
            return False

        import time
        interpreter.ds = Stack(*interpreter.ds, int(time.time() * 1000))
        interpreter.cs = Stack(*rcs)
        return True

class OperatingSystem(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
        except ValueError:
            return False

        if cw != "operating-system":
            return False

        import platform

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*interpreter.ds, platform.platform())
        return True

class IsInteger(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, num = interpreter.ds
        except ValueError:
            return False

        if cw != "integer?":
            return False

        try:
            result = int(num)
        except (ValueError, TypeError):
            result = "f"

        result = "t" if result != "f" else "f"

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class Addition(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != "+":
                return False

            result = str(int(x)+int(y))
        except (ValueError, TypeError):
            return False

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class Subtraction(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != "-":
                return False

            result = str(int(x)-int(y))
        except (ValueError, TypeError):
            return False

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class Multiplication(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != "*":
                return False

            result = str(int(x)*int(y))
        except (ValueError, TypeError):
            return False

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class Devision(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != "div":
                return False

            result = str(int(x)//int(y))
        except (ValueError, TypeError):
            return False

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class Modulus(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != "mod":
                return False

            result = str(int(x)%int(y))
        except (ValueError, TypeError):
            return False

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class LessThan(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != "<":
                return False

            result = int(x) < int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class MoreThan(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != ">":
                return False

            result = int(x) > int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class MoreThanEqual(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != ">=":
                return False

            result = int(x) >= int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class LessThanEqual(NativeRule):
    def execute(self, interpreter: Interpreter):
        try:
            cw, *rcs = interpreter.cs
            *rds, x, y = interpreter.ds

            if cw != "<=":
                return False

            result = int(x) <= int(y)
        except (ValueError, TypeError):
            return False

        result = "t" if result else "f"

        interpreter.cs = Stack(*rcs)
        interpreter.ds = Stack(*rds, result)
        return True

class DefineAliasRule(NativeRule):
    """
    Define an alias rule and add it to the ruleset.
    """

    def name(self) -> str:
        return "def"

    def execute(self, interpreter):
        _, r = RuleParser.parse("#ALIAS [ @BODY ] | def ->")
        m = r.matches(interpreter=interpreter)
        if not m:
            _, r = RuleParser.parse("#ALIAS #WRD | def ->")
            m = r.matches(interpreter=interpreter)
            if not m:
                return False

        alias = m["#ALIAS"]
        body = m["@BODY"] if "@BODY" in m else Stack(m["#WRD"])

        nr = AliasRule(alias=alias, words=body)
        err = interpreter.ruleset.prepand(nr)
        if err:
            interpreter.print_error(err.msg)
            return False

        # Apply changes to stacks
        r.instantiate(data=m, interpreter=interpreter)
        return True
