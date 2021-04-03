

from ..classes import Ref
from .Function import Fun



class Context:
    def __init__(self) -> None:
        # will be used to store: ref -> code line
        self.refDict = {}
        self.refCount = 0
        self.fun = Fun(self)
        self.funs = {}
        self.nextNoVar = 0

    def clear(self):
        self.refDict = {}
        self.refCount = 0
        self.fun = Fun(self)
        self.funs = {}
        self.nextNoVar = 0

    def registerFun(self):
        if self.fun.name in self.funs:
            raise SystemExit("function {} already defined".format(self.fun.name))

        self.funs[self.fun.name] = self.fun
        self.fun = Fun(self)  # clean context fun scope

    def addRef(self, ref, index):
        if ref.id in self.refDict:
            raise Exception('ref {} already declared'.format(ref.id))
        self.refDict[ref.id] = index

    def genRef(self):
        self.refCount += 1
        return Ref(self.refCount)
