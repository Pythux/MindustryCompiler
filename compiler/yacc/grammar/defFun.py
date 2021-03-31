from boa import boa
from ._start import grammar, YaccProduction, context


@grammar
def runFunc(p: YaccProduction):
    '''lines : ID OpenParenthesis argumentsCall CloseParenthesis'''
    funName = p[1]
    callArgs = p[3]
    if funName not in context.funs:
        raise SystemExit("function '{}' does not exist at line {}".format(funName, p.lineno(1)))
    fun = context.funs[funName]
    lines = []
    lines += setFunctionCallArgs(fun, callArgs)
    lines += fun.content
    p[0] = lines


def setFunctionCallArgs(fun, callArgs):
    return ['set {} {}'.format(fun.ids[farg], carg) for farg, carg in zip(fun.args, callArgs)]


@grammar
def argumentsCall(p: YaccProduction):
    '''argumentsCall : ID'''
    p[0] = [p[1]]


@grammar
def argumentsCall_many(p: YaccProduction):
    '''argumentsCall : argumentsCall Comma ID'''
    p[0] = p[1] + [p[3]]


@grammar
def argumentsCall_empty(p: YaccProduction):
    '''argumentsCall : '''
    p[0] = []

@grammar
def defFun(p: YaccProduction):
    '''noLine : DefFun ID funScope OpenParenthesis arguments CloseParenthesis OpenCurlyBracket lines CloseCurlyBracket'''
    name = p[2]
    content = p[8]
    context.registerFun(name, content)


@grammar
def funScope(p: YaccProduction):
    '''funScope :'''
    if context.fun.inFunScope:
        print("function definition inside function is not handled")
        raise SystemExit()
    context.fun.inFunScope = True


@grammar
def args(p: YaccProduction):
    '''arguments : ID'''
    arg = p[1]
    addArgument(arg)


@grammar
def args_many(p: YaccProduction):
    '''arguments : arguments Comma ID'''
    arg = p[3]
    addArgument(arg)


@grammar
def args_empty(p: YaccProduction):
    '''arguments : '''


def addArgument(arg):
    if arg in context.fun.args:
        raise SystemExit('Duplicate parameter "{}"'.format(arg))
    context.fun.args.append(arg)
    context.fun.scopeId(arg)
