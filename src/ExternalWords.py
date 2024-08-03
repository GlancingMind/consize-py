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
            result = subprocess.run([word, *interpreter.ds], capture_output=True, text=True)
            if result.returncode == 0:
                interpreter.cs = rcs
                interpreter.ds = parse(result.stdout)
                return True

        return False


from abc import ABC
import importlib
import sys


class ExternalWord(ABC):
    # TODO add abstract methode, which the external word should have

class ExternalWordModules(ABC):

    def __init__(self, modules: list[str]):
        self.module_specs = { os.path.basename(module): module for module in modules }
        for name, path in self.module_specs:
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None:
                raise ImportError(f"Cannot load spec for {name} from {path}")

            module = importlib.util.module_from_spec(spec)
            sys.modules[module] = module
            spec.loader.exec_module(module)
            extWrds = ExternalWords.__subclasses__()
            for extWrd in extWrds:
                interpreter = extWrd.execute(interpreter)
