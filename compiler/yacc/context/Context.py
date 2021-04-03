

from ..classes import Jump, Ref


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


class Fun:
    def __init__(self, context) -> None:
        self.name = None
        self.inFunScope = False
        self.idCount = 0
        self.ids = {}
        self.args = []
        self.refs = {}
        self.returns = None
        self.returnRef = None
        self.content = []
        self.context = context

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

    def scopeRef(self, ref):
        if ref not in self.refs:
            self.refs[ref] = self.context.genRef().id
        return self.refs[ref]

    # change ref for multiple copie/paste
    def genContent(self):
        newRef = {}
        lines = []
        for line in self.content:
            if isinstance(line, Ref):
                if line.id not in newRef:
                    newRef[line.id] = self.context.genRef()
                line = newRef[line.id]
            elif isinstance(line, Jump):
                if line.ref.id not in newRef:
                    newRef[line.ref.id] = self.context.genRef()
                # j = copy.copy(line)
                j = Jump(line.line, newRef[line.ref.id])
                # j.ref = newRef[line.ref.id]
                # j.line = line.line
                j.asmCondition = line.asmCondition
                line = j
            lines.append(line)

        if self.returnRef.id in newRef:
            self.returnRef = newRef[self.returnRef.id]
        else:
            self.returnRef = self.context.genRef()
        return lines
