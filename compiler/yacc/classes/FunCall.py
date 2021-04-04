

from ..importsHandling import imports


class FunCall:
    def __init__(self, funName, callArgs, line, returnTo=None, module=None) -> None:
        self.funName = funName
        self.callArgs = callArgs
        self.returnTo = returnTo
        self.line = line
        self.module = module

    def toFunContent(self):
        module = imports.getModule(self.module)
        if self.funName not in module:
            raise SystemExit("function '{}' does not exist at line {}".format(self.funName, self.line))
        fun = module[self.funName]
        lines = []
        lines += setters(map(lambda a: fun.ids[a], fun.args), self.callArgs)
        lines += fun.genContent()
        lines.append(fun.returnRef)
        if self.returnTo:
            if len(self.returnTo) != len(fun.returns):
                raise SystemExit('function “{}” return exactly {} values, {} is receved line {}'
                                 .format(fun.name, len(fun.returns), len(self.returnTo), self.line))
            lines += setters(self.returnTo, fun.returns)
        return lines


def setters(liSet, liVar):
    'set {liSet} {liVal}'
    return ['set {} {}'.format(s, v) for s, v in zip(liSet, liVar)]
