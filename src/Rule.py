from abc import ABC, abstractmethod
from dataclasses import dataclass

import Stack
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
        return self.__class__.__name__.lower()

    def description(self) -> str:
        return self.__class__.__doc__ or \
        """
        No Description Provided.
        """

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

class AliasRule(IRule):
    def __init__(self, alias: str, words: Stack.Stack):
        self.alias = alias
        self.words = words

    def name(self) -> str:
        return self.alias

    def description(self) -> str:
        return f"{self.alias} -> | {self.words.toString(addEnclosingParenthesis=False)}"

    def execute(self, interpreter) -> bool:
        if interpreter.cs != [] and interpreter.cs.peek() == self.alias:
            interpreter.cs.pop(0)
            interpreter.cs = Stack.Stack(*self.words, *interpreter.cs)
            return True
        return False

    def __repr__(self) -> str:
        return self.description()
