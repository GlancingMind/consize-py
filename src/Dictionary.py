class Dictionary(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "{"+" ".join(self)+"}"

    def contains(self, k: str, v: str) -> bool:
        return self._data[self.index(k)+1] == v

    # def items(self) -> zip[tuple[str, str]]:
    #     return zip(self._data[::2],self._data[1::2])

    # def __eq__(self, other):
    #     if not isinstance(other, Dictionary):
    #         return False

    #     if len(self) != len(other):
    #         return False

    #     for i in self.items:
    #         if not other.contains(i[0], i[1]):
    #             return False

    #     return True

    def __setitem__(self, key, value):
        # Check if the key already exists and update the value if it does
        for i, (k, v) in enumerate(self._data):
            if k == key:
                self._data[i] = (key, value)
                return
        # Otherwise, add a new key-value pair
        self._data.append((key, value))
