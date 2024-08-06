from dataclasses import dataclass

import StackPattern

@dataclass
class Rule():
    dsp: StackPattern
    csp: StackPattern
    dst: StackPattern
    cst: StackPattern
    rule_desc: str

    def __repr__(self) -> str:
        if self.rule_desc:
            return self.rule_desc
        return f"{self.dsp} | {self.csp} -> {self.dst} | {self.cst}"

    def execute(self, interpreter):
        csm = StackPattern.match(self.csp, interpreter.cs, topOfStackIsLeft=True)
        dsm = StackPattern.match(self.dsp, interpreter.ds)
        if not csm or not dsm:
            return False
        matches = csm | dsm
        interpreter.cs = StackPattern.instantiate(self.cst, matches)
        interpreter.ds = StackPattern.instantiate(self.dst, matches)
        return True
