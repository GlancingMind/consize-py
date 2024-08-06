from abc import ABC, abstractmethod
import importlib as importlib
import sys

from Rule import Rule
from Interpreter import Interpreter

class ExternalWord(ABC):
    @abstractmethod
    def execute(self, i: Interpreter):
        pass

class ExternalWordModules(Rule):

    def __init__(self, moduleDir: str):
        for module_name in os.listdir(moduleDir):
            module_path = os.path.join(moduleDir, module_name)
            if not os.path.isfile(module_path):
                continue

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is None:
                raise ImportError(f"Cannot load module from {module_path}")

            module = importlib.util.module_from_spec(spec)
            sys.modules[module] = module
            spec.loader.exec_module(module)
            self.extWrds = ExternalWord.__subclasses__()

    def execute(self, interpreter):
        for extWrd in self.extWrds:
            if extWrd.execute(interpreter):
                return True
        return False

    def __repr__(self) -> str:
        return "ext-word"


#########################################################################
# PROTOTYPE to execute external words implemented in arbitary languages.
# This does currently only support datastack manipulation.
# Callstack manipulation isn't possible due to missing data exchange format.

import importlib.util
import os
import subprocess

from Interpreter import Interpreter
from Rule import Rule
from StackParser import parse

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

    def __repr__(self) -> str:
        return "ext-word"
