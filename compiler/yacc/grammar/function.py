
from compiler.yacc.classes import Jump, FunCall
from ._start import grammar, YaccProduction, context


@grammar
def runFunc(p: YaccProduction):
    '''lines : ID OpenParenthesis argumentsCall CloseParenthesis'''
    funName = p[1]
    callArgs = p[3]
    p[0] = FunCall(funName, callArgs)


@grammar
def runFuncReturnArgs(p: YaccProduction):
    '''lines : returnedVars Affectaction ID OpenParenthesis argumentsCall CloseParenthesis'''
    returnTo = p[1]
    funName = p[3]
    callArgs = p[5]
    p[0] = FunCall(funName, callArgs, returnTo, p.lineno(1))


@grammar
def defFun(p: YaccProduction):
    '''noLine : DefFun funName funScope OpenParenthesis arguments CloseParenthesis OpenCurlyBracket lines CloseCurlyBracket'''
    content = p[8]
    context.fun.content = content
    context.registerFun()


@grammar
def funName(p: YaccProduction):
    '''funName : ID'''
    context.fun.name = p[1]


@grammar
def funScope(p: YaccProduction):
    '''funScope : '''
    if context.fun.inFunScope:
        print("function definition inside function is not handled")
        raise SystemExit()
    context.fun.inFunScope = True

    context.fun.returnRef = context.genRef()


@grammar
def handleReturn(p: YaccProduction):
    '''lines : Return returnsVal'''
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


def setters(liSet, liVar):
    'set {liSet} {liVal}'
    return ['set {} {}'.format(s, v) for s, v in zip(liSet, liVar)]
