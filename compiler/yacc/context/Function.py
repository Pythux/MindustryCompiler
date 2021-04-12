
from ..classes import Jump, Ref, AsmInst, Variable, Value


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
        self.jumpDefinition = None
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

    def scopeRef(self, ref):
        if ref not in self.refs:
            self.refs[ref] = self.context.genRef().id
        return self.refs[ref]

    # change ref/var name for scope
    def generateDefinition(self):
        if self.defined:
            raise Exception("function {} is already defined".format(self.name))
        self.defined = True
        self.jumpDefinition = self.context.genRef()
        lines = self.content

        if self.returnRef:
            lines.append(self.returnRef)
        # jump to funCall
        lines.append(AsmInst('set', [Value('@counter'), Variable('returnAddress')]))
        return lines
