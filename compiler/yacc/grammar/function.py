from compiler.yacc.grammar.contextAndClass import Jump
from ._start import grammar, YaccProduction, context


@grammar
def runFunc(p: YaccProduction):
    '''lines : ID OpenParenthesis argumentsCall CloseParenthesis'''
    funName = p[1]
    callArgs = p[3]
    p[0] = toFunContent(funName, callArgs)


@grammar
def runFuncReturnArgs(p: YaccProduction):
    '''lines : returnedVars Affectaction ID OpenParenthesis argumentsCall CloseParenthesis'''
    returnTo = p[1]
    funName = p[3]
    callArgs = p[5]
    p[0] = toFunContent(funName, callArgs, returnTo, p.lineno(1))


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


@grammar
def returnedVars_one(p: YaccProduction):
    '''returnedVars : ID'''
    p[0] = [p[1]]


@grammar
def returnedVars_many(p: YaccProduction):
    '''returnedVars : returnedVars Comma ID'''
    p[0] = p[1] + [p[3]]


@grammar
def argumentsCall(p: YaccProduction):
    '''argumentsCall : info'''
    p[0] = [p[1]]


@grammar
def argumentsCall_many(p: YaccProduction):
    '''argumentsCall : argumentsCall Comma info'''
    p[0] = p[1] + [p[3]]


@grammar
def argumentsCall_empty(p: YaccProduction):
    '''argumentsCall : '''
    p[0] = []


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


@grammar
def handleReturn(p: YaccProduction):
    '''lines : Return returnsVal'''
    if not context.fun.inFunScope:
        print("return keyword only indide function definition, line {}".format(p.lineno(1)))
        raise SystemExit()
    p[0] = funReturn(p[2])


@grammar
def returnsVal_empty(p: YaccProduction):
    '''returnsVal : '''
    p[0] = []


@grammar
def returnsVal_one(p: YaccProduction):
    '''returnsVal : info'''
    p[0] = [p[1]]


@grammar
def returnsVal_many(p: YaccProduction):
    '''returnsVal : returnsVal Comma info'''
    p[0] = p[1] + [p[3]]


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
