from collections import UserList, UserString
from typing import Union

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

class Dictionary(UserList):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        stringifiedElements = [str(itm) for itm in self.data]
        result = (" ").join(["{",*stringifiedElements,"}"])
        return result

    def copy(self) -> list:
        return Dictionary(*self.data)

# TODO Use Word-Type instead of string. This will probably result in a complete
# rewrite of every unit test, as every str might be wrapped into a Word...
class Word(UserString):
    def __init__(self, seq: object) -> None:
        super().__init__(seq)

    def __repr__(self):
        return self.data

    def copy(self) -> list:
        return Word(self.data)

StackElement = Union[Stack, Dictionary, str]
