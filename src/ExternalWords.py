import os
import subprocess

from Rule import Rule
from StackDeserializer import parse

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
                interpreter.ds = parse(result.stdout)
                return True

        return False
