from abc import ABC, abstractmethod
from dataclasses import dataclass

import StackPattern

class IRule(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, interpreter) -> bool|dict:
        pass

class NativeRule(IRule):
    def name(self) -> str:
        return self.__qualname__

    def description(self) -> str:
        return self.__doc__

@dataclass
class Rule(IRule):
    dsp: StackPattern
    csp: StackPattern
    dst: StackPattern
    cst: StackPattern
    rule_desc: str

    def name(self) -> str:
        return ""

    def description(self) -> str:
        return ""

    def __repr__(self) -> str:
        if self.rule_desc:
            return self.rule_desc
        return f"{self.dsp} | {self.csp} -> {self.dst} | {self.cst}"

    def matches(self, interpreter):
        csm = StackPattern.match(self.csp, interpreter.cs, topOfStackIsLeft=True)
        dsm = StackPattern.match(self.dsp, interpreter.ds)
        if not csm or not dsm:
            return False
        return csm | dsm

    def execute(self, interpreter):
        matches = self.matches(interpreter)
        if matches == False:
            return False
        return self.instantiate(matches, interpreter)

    def instantiate(self, data: dict, interpreter):
        if data == False:
            return False
        interpreter.cs = StackPattern.instantiate(self.cst, data)
        interpreter.ds = StackPattern.instantiate(self.dst, data)
        return True
