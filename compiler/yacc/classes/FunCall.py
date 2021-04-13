

from ..importsHandling import imports
from .AsmInst import AsmInst, Value, Variable
from .RefAndJump import Jump


class FunCall:
    def __init__(self, module, name, callArgs, line, returnTo=None) -> None:
        self.name = name
        self.callArgs = callArgs
        self.returnTo = returnTo if returnTo is not None else []
        self.line = line
        self.module = module if module else imports.currentFile

    def toContent(self):
        fun = imports.getFunCalled(self.module, self.name, self.line)
        return self.toFunContent(fun)

    def toFunContent(self, fun):
        lines = []
        lines += setters(map(lambda a: fun.ids[a], fun.args), self.callArgs)
        lines.append(AsmInst('op', [Value('add'), fun.returnAddress, Value('@counter'), Value('1')]))
        lines.append(Jump('jump to function {}'.format(self.name), fun.refDefinition))
        # function returned
        # set tmp to var return
        if len(self.returnTo):
            if len(self.returnTo) != len(fun.returns):
                raise Exception('function “{}” return exactly {} values, {} is receved line {}'
                                .format(fun.name, len(fun.returns), len(self.returnTo), self.line))
            lines += setters(self.returnTo, fun.returns)
        return lines

    def copy(self):
        # return self
        callArgs = self.callArgs.copy()
        returnTo = self.returnTo.copy()
        return self.__class__(self.module, self.name, callArgs, self.line, returnTo)

        # replace an ID by another (ID or info)
    def replace(self, toReplace, toReplaceBy):
        for index, arg in enumerate(self.callArgs):
            if isinstance(arg, Variable) and arg == toReplace:
                self.callArgs[index] = toReplaceBy

        for index, arg in enumerate(self.returnTo):
            if isinstance(arg, Variable) and arg == toReplace:
                self.returnTo[index] = toReplaceBy

    def __str__(self) -> str:
        return "<FunCall {}.{}>".format(self.module, self.name)


# set {liSet} {liVal}
def setters(liSet, liVar):
    return [AsmInst('set', [s, v]) for s, v in zip(liSet, liVar)]
