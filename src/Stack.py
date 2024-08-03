from collections import UserList

# TODO maybe switch to Deque for performance, as at matcher will result in
# popping from other stack side.
class Stack(UserList):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        stringifiedElements = [str(itm) for itm in self.data]
        result = (" ").join(["[",*stringifiedElements,"]"])
        return result

    def copy(self) -> list:
        return Stack(*self.data)
