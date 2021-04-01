

class Context:
    def __init__(self) -> None:
        # will be used to store: ref -> code line
        self.refDict = {}
        self.refCount = 0
        self.fun = Fun()
        self.funs = {}

    def clear(self):
        self.refDict = {}
        self.refCount = 0
        self.fun = Fun()
        self.funs = {}

    def registerFun(self):
        if self.fun.name in self.funs:
            raise SystemExit("function {} already defined".format(self.fun.name))

        self.funs[self.fun.name] = self.fun
        self.fun = Fun()  # clean context fun scope

    def addRef(self, ref, index):
        if ref.id in self.refDict:
            raise Exception('ref {} already declared'.format(ref.id))
        self.refDict[ref.id] = index

    def genRef(self):
        self.refCount += 1
        return Ref(self.refCount)


class Fun:
    def __init__(self) -> None:
        self.name = None
        self.inFunScope = False
        self.idCount = 0
        self.ids = {}
        self.args = []
        self.returns = None
        self.returnRef = None
        self.content = []

    def scopeId(self, identifier):
        if identifier not in self.ids:
            self.ids[identifier] = self.genId()
        return self.ids[identifier]

    def genId(self):
        self.idCount += 1
        newId = 'tmp{}'.format(self.idCount)
        if newId not in self.ids:
            return newId
        return self.genId()


context = Context()


class Ref:
    def __init__(self, ref: str) -> None:
        self.id = ref

    def __str__(self) -> str:
        return "<Ref: {}>".format(self.id)

    def __repr__(self) -> str:
        return self.__str__()


class Jump:
    def __init__(self, line, ref: Ref, condition=None) -> None:
        self.line = line
        self.ref = ref
        self.asmCondition = condition if condition is not None else 'always true true'

    def toLine(self):
        if self.ref.id not in context.refDict:
            print("for jump at line: {}".format(self.line))
            print("ref {} not exist, existing ref: {}".format(self.ref.id, context.refDict))
            raise SystemExit()
        return 'jump {ref} {condition}'.format(
            ref=context.refDict[self.ref.id], condition=self.asmCondition)

    def __str__(self):
        return '<Jump: {} {}>'.format(self.ref, self.asmCondition)

    def __repr__(self) -> str:
        return self.__str__()
