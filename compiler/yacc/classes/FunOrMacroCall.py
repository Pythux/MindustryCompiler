

from ..importsHandling import imports
from .Macro import Macro


class FunOrMacroCall:
    def __init__(self, module, name, callArgs, line, returnTo=None) -> None:
        self.name = name
        self.callArgs = callArgs
        self.returnTo = returnTo
        self.line = line
        self.module = module if module else imports.currentFile

    def toContent(self):
        module = imports.getModule(self.module)
        if self.name not in module:
            raise Exception("function '{}' does not exist, module {}, at line {}"
                            .format(self.name, self.module, self.line))
        funOrMacro = module[self.name]

        if isinstance(funOrMacro, Macro):
            return self.toMacroContent(funOrMacro)
        return self.toFunContent(funOrMacro)

    def toFunContent(self, fun):
        lines = []
        lines += setters(map(lambda a: fun.ids[a], fun.args), self.callArgs)
        lines += fun.genContent()
        if self.returnTo:
            if len(self.returnTo) != len(fun.returns):
                raise Exception('function “{}” return exactly {} values, {} is receved line {}'
                                .format(fun.name, len(fun.returns), len(self.returnTo), self.line))
            lines += setters(self.returnTo, fun.returns)
        return lines

    def toMacroContent(self, macro):
        pass


def setters(liSet, liVar):
    'set {liSet} {liVal}'
    return ['set {} {}'.format(s, v) for s, v in zip(liSet, liVar)]
