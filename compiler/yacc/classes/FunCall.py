

from ..importsHandling import imports
from .AsmInst import AsmInst, Value, Variable
from .RefAndJump import Jump


class FunCall:
    def __init__(self, module, name, callArgs, line, returnTo=None) -> None:
        self.name = name
        self.callArgs = callArgs
        self.returnTo = returnTo
        self.line = line
        self.module = module if module else imports.currentFile

    def toContent(self):
        fun = imports.getFunCalled(self.module, self.name, self.line)
        return self.toFunContent(fun)

    def toFunContent(self, fun):
        lines = []
        lines += setters(map(lambda a: fun.ids[a], fun.args), self.callArgs)
        lines.append(AsmInst('add', [Variable('returnAddress'), Value('@counter'), Value('1')]))
        lines.append(Jump('jump to function {}'.format(self.name), fun.jumpDefinition))
        # function returned
        # set tmp to var return
        if self.returnTo:
            if len(self.returnTo) != len(fun.returns):
                raise Exception('function “{}” return exactly {} values, {} is receved line {}'
                                .format(fun.name, len(fun.returns), len(self.returnTo), self.line))
            lines += setters(self.returnTo, fun.returns)
        return lines


# set {liSet} {liVal}
def setters(liSet, liVar):
    return [AsmInst('set', [s, v]) for s, v in zip(liSet, liVar)]
