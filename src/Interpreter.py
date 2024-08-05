from Stack import Stack

class Interpreter:

    def __init__(self, cs: Stack = [], ds: Stack = [], maxRecursionDepth=20, trunkPrintOfStackToLength=0):
        self.ds = ds
        self.cs = cs
        self.maxRecursionDepth=maxRecursionDepth
        self.trunkPrintOfStackToLength=trunkPrintOfStackToLength
