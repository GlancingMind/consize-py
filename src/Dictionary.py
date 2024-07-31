class Dictionary(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        str = self.stringify_stack(self)
        return "{"+str+"}"

    def stringify_stack(self, lst):
        return ' '.join(self.stringify_stack(item) if isinstance(item, list) else str(item) for item in lst)

    def copy(self) -> list:
        return Dictionary(super().copy())
