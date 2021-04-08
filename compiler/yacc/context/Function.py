
from ..classes import Jump, Ref, Variable


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
                j = Jump(line.line, newRef[line.ref.id])
                j.asmCondition = line.asmCondition
                line = j
            lines.append(line)

        if self.returnRef.id in newRef:
            returnRef = newRef[self.returnRef.id]
        else:
            returnRef = self.context.genRef()

        lines.append(returnRef)
        return lines
