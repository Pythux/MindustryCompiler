
from compiler import CompilationException
from .AsmInst import AsmInst
from .ValVarKey import Value, Variable
from .RefAndJump import Ref, Jump


class ReturnStm:
    def __init__(self, variables) -> None:
        self.variables = variables

    def __repr__(self) -> str:
        return '<ReturnStm {}>'.format(self.variables)

    def __len__(self) -> int:
        return len(self.variables)

    def __iter__(self):
        return iter(self.variables)


class FunDef:
    def __init__(self, context, name, args, content) -> None:
        self.context = context
        self.name = name
        self.args = args
        self.content = content

        self.ids = {}
        self.refs = {}
        self.returns = None
        self.returnRef = None
        self.refDefinition = None
        self.defined = False
        self.processReturns()
        self.scopeVarRef()

    # return line to lines
    def processReturns(self):
        newContent = []
        for line in self.content:
            if isinstance(line, ReturnStm):
                newContent += self.genReturnLines(line)
            else:
                newContent.append(line)
        self.content = newContent

    def genReturnLines(self, returnStm: ReturnStm):
        if self.returns is None:  # no return meet before, generates liste of vars to return
            self.returns = [self.genId() for _ in range(len(returnStm))]
            self.returnRef = self.context.genRef()

        lines = setters(self.returns, returnStm)
        lines.append(Jump('return', self.returnRef))
        return lines

    # scope fun args / content
    def scopeVarRef(self):
        for line in self.content:
            line.applyToVariables(self.scopeId)
            if isinstance(line, Ref) or isinstance(line, Jump):
                line.applyToRef(self.scopeRef)

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
            raise CompilationException("function {} is already defined".format(self.name))
        self.defined = True
        self.refDefinition = self.context.genRef()
        self.returnAddress = self.getReturnAddr(moduleName)
        lines = [self.refDefinition] + self.content

        if self.returnRef:
            lines.append(self.returnRef)
        # jump to funCall
        lines.append(AsmInst('set', [Value('@counter'), self.returnAddress]))
        return lines


# set {liSet} {liVal}
def setters(liSet, liVar):
    return [AsmInst('set', [s, v]) for s, v in zip(liSet, liVar)]
