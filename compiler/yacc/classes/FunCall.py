

from ..Imports import imports


class FunCall:
    def __init__(self, funName, callArgs, returnTo=None, line=None) -> None:
        self.funName = funName
        self.callArgs = callArgs
        self.returnTo = returnTo
        self.line = line

    def toFunContent(funName, callArgs, returnTo=None, line=None):
        if funName not in context.funs:
            raise SystemExit("function '{}' does not exist at line {}".format(funName, line))
        fun = context.funs[funName]
        lines = []
        lines += setters(map(lambda a: fun.ids[a], fun.args), callArgs)
        lines += fun.genContent()
        lines.append(fun.returnRef)
        if returnTo:
            if len(returnTo) != len(fun.returns):
                raise SystemExit('function “{}” return exactly {} values, {} is receved line {}'
                                 .format(fun.name, len(fun.returns), len(returnTo), line))
            lines += setters(returnTo, fun.returns)
        return lines


def setters(liSet, liVar):
    'set {liSet} {liVal}'
    return ['set {} {}'.format(s, v) for s, v in zip(liSet, liVar)]
