
from ..classes import AsmInst, Variable, Value


class Fun:
    def __init__(self, context) -> None:
        self.name = None
        self.inFunScope = False
        self.ids = {}
        self.args = []
        self.refs = {}
        self.returns = None
        self.returnRef = None
        self.content = []
        self.context = context
        self.refDefinition = None
        self.defined = False

    def scopeId(self, identifier: Variable):
        if identifier not in self.ids:
            self.ids[identifier] = self.genId()
        return self.ids[identifier]

    def genId(self):
        self.context.idInc += 1
        newId = Variable('tmp{}'.format(self.context.idInc))
        if newId not in self.context.existingVars:
            return newId
        return self.genId()

    def getReturnAddr(self, moduleName, idInc=None) -> Variable:
        if idInc is None:
            idInc = 0
            newId = Variable('returnAddress-{}-{}'.format(moduleName, self.name))
        else:
            newId = Variable('returnAddress-{}-{}-{}'.format(moduleName, self.name, idInc))

        if newId not in self.context.existingVars:
            self.context.existingVars.add(newId)
            return newId
        return self.getReturnAddr(moduleName, idInc+1)

    def scopeRef(self, ref):
        if ref not in self.refs:
            self.refs[ref] = self.context.genRef().id
        return self.refs[ref]

    # change ref/var name for scope
    def generateDefinition(self, moduleName):
        if self.defined:
            raise Exception("function {} is already defined".format(self.name))
        self.defined = True
        self.refDefinition = self.context.genRef()
        self.returnAddress = self.getReturnAddr(moduleName)
        lines = [self.refDefinition] + self.content

        if self.returnRef:
            lines.append(self.returnRef)
        # jump to funCall
        lines.append(AsmInst('set', [Value('@counter'), self.returnAddress]))
        return lines
