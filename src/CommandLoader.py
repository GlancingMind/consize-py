from abc import ABC, abstractmethod
import importlib as importlib
import os
import sys

from Rule import Rule
from Interpreter import Interpreter

class Command(ABC):
    @abstractmethod
    def execute(self, i: Interpreter):
        pass

class CommandLoader(Rule):

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
            self.cmds = Command.__subclasses__()

    def execute(self, interpreter):
        for cmd in self.cmds:
            if cmd.execute(interpreter):
                return True
        return False

    def __repr__(self) -> str:
        return str(Command)
