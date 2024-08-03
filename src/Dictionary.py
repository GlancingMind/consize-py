from collections import UserList

class Dictionary(UserList):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        stringifiedElements = [str(itm) for itm in self.data]
        result = (" ").join(["{",*stringifiedElements,"}"])
        return result

    def copy(self) -> list:
        return Dictionary(*self.data)
