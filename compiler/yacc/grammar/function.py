
from compiler.yacc.classes import Jump, FunCall
from ._start import grammar, YaccProduction, context

from .. import importsHandling
from ..classes import AsmInst


def getModuleAndFunName(dotted):
    module = None
    if len(dotted) == 2:
        module, funName = dotted
    else:
        assert len(dotted) == 1
        funName = dotted[0]
    return module, funName


@grammar
def runFuncReturnArgs(p: YaccProduction):
    '''line : affectation dottedID OpenParenthesis arguments CloseParenthesis'''
    returnTo = p[1]
    returnTo = handleScopeReturnedVars(returnTo)
    dotted = p[2]
    module, funName = getModuleAndFunName(dotted)
    callArgs = p[4]
    p[0] = FunCall(module, funName, callArgs, p.lineno(1), returnTo)


def handleScopeReturnedVars(liReturn):
    if context.fun.inFunScope:
        return [context.fun.scopeId(arg) for arg in liReturn]
    return liReturn


@grammar
def runFunc(p: YaccProduction):
    '''line : dottedID OpenParenthesis arguments CloseParenthesis'''
    dotted = p[1]
    module, funName = getModuleAndFunName(dotted)
    callArgs = p[3]
    p[0] = FunCall(module, funName, callArgs, p.lineno(1))


@grammar
def defFun(p: YaccProduction):
    '''noLine : dottedID OpenParenthesis arguments CloseParenthesis OpenCurlyBracket funScope lines CloseCurlyBracket''' # noqa
    if len(p[1]) != 1:
        raise Exception("function definition incorrect: {} is not accepted".format(p[1]))
    context.fun.name = p[1][0]
    args = p[3]
    addArguments(args)
    content = p[7]
    context.fun.content = content
    importsHandling.imports.addFunToModule(context.getDefinedFunction())


# register function definition arguments
def addArguments(args):
    for arg in args:
        if arg in context.fun.args:
            raise SystemExit('Duplicate parameter "{}"'.format(arg))
        context.fun.args.append(arg)
        context.fun.scopeId(arg)


@grammar
def funScope(p: YaccProduction):
    '''funScope : '''
    if context.fun.inFunScope:
        print("function definition inside function is not handled line: {}".format(p.lineno(0)))
        raise SystemExit()
    context.fun.inFunScope = True

    context.fun.returnRef = context.genRef()


@grammar
def handleReturn(p: YaccProduction):
    '''lines : Return arguments'''
    if not context.fun.inFunScope:
        print("return keyword only indide function definition, line {}".format(p.lineno(1)))
        raise SystemExit()
    p[0] = funReturn(p[2])


def funReturn(args):
    if context.fun.returns is None:
        # no return meet before
        context.fun.returns = [context.fun.genId() for _ in range(len(args))]

    # exact same return quantity
    if len(args) != len(context.fun.returns):
        raise SystemExit("function {} must return {} as many values for all it's return"
                         .format(context.fun.name, len(context.fun.returns)))

    lines = setters(context.fun.returns, args)
    lines.append(Jump('return', context.fun.returnRef))
    return lines


# set {liSet} {liVal}
def setters(liSet, liVar):
    return [AsmInst('set', [s, v]) for s, v in zip(liSet, liVar)]
