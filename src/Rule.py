from dataclasses import dataclass

import StackPattern

@dataclass
class Rule:
    dsp: StackPattern
    csp: StackPattern
    dst: StackPattern
    cst: StackPattern

    def __repr__(self) -> str:
        return f"{self.mp} | {self.cs} -> {self.nds} | {self.ncs}"

    def execute(self, interpreter):
        csm = StackPattern.match(self.csp, interpreter.cs, topOfStackIsLeft=True)
        dsm = StackPattern.match(self.dsp, interpreter.ds)
        if not csm or not dsm:
            return False
        matches = csm | dsm
        interpreter.cs = StackPattern.instantiate(self.cst, matches)
        interpreter.ds = StackPattern.instantiate(self.dst, matches)
        return True
