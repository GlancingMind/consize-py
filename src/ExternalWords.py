import os
import subprocess

from Dictionary import Dictionary
from Rule import Rule

class ExternalWords(Rule):

    def __init__(self, wordScripts: list[str]):
        self.words = { os.path.basename(script): script for script in wordScripts }


    def execute(self, interpreter):
        if interpreter.cs == []:
            return False

        *rcs, wc = interpreter.cs
        if self.words == []:
            return False

        if wc in self.words:
            word = self.words[wc]
            result = subprocess.run([word] + interpreter.ds, capture_output=True, text=True)
            if result.returncode == 0:
                interpreter.cs = rcs
                interpreter.ds = self.__parsePattern(result.stdout)
                return True

        return False

    def __parsePattern(self, tokens: str):
        pattern = []
        while tokens != []:
            token, *tokens = tokens
            if token == "[":
                p, tokens = self.__parsePattern(tokens)
                pattern.append(p)
            elif token == "]":
                return pattern, tokens
            elif token == "{":
                p, tokens = self.__parseDict(tokens)
                pattern.append(p)
            elif token.strip() == "":
                continue
            else:
                pattern.append(token)
        return pattern

    def __parseDict(self, tokens: str):
        d = Dictionary()
        while tokens != []:
            token, *tokens = tokens
            if token == "{":
                d, tokens = self.__parseDict(tokens)
                d.append(d)
            elif token == "}":
                break
            elif token.strip() == "":
                continue
            else:
                value, tokens = self.__parsePattern([token])
                # The result of __parsePattern will be always a stack.
                # Therefore __parsePattern([b]) for { a b }, will return [b].
                # But what we want is the unwrapped b, therefore we unwrap it.
                # What if { a [ b ] } is given?
                # Then __parsePattern will return
                # [[b]], which will be unwrapped, yielding the correct value [b].
                if len(value) == 1:
                    d.append(value[0])
                else:
                    d.append(value)

        return d
