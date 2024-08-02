class Stack(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return (" ").join(["[",*self,"]"])

    def copy(self) -> list:
        return Stack(super().copy())
