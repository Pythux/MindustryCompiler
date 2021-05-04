
from compiler import CompilationException
from ..classes import Ref, Variable


class Context:
    def __init__(self) -> None:
        # will be used to store: ref -> code line
        self.refDict = {}
        self.refCount = 0
        self.existingVars = set()
        self.idInc = 0
        self.staticVarsList = {}
        self.inFunDefinition = False

    def clear(self):
        self.refDict = {}
        self.refCount = 0
        self.existingVars = set()
        self.idInc = 0
        self.staticVarsList = {}
        self.inFunDefinition = False

    def addRef(self, ref, index):
        if ref.id in self.refDict:
            raise CompilationException('ref {} already declared'.format(ref.id))
        self.refDict[ref.id] = index

    def genRef(self):
        self.refCount += 1
        return Ref(self.refCount)

    def genId(self):
        self.idInc += 1
        newId = Variable('tmp{}'.format(self.idInc))
        if newId not in self.existingVars:
            return newId
        return self.genId()
