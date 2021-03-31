from boa import boa
from ._start import grammar, YaccProduction, context


@grammar
def runFunc(p: YaccProduction):
    '''lines : ID OpenParenthesis arguments CloseParenthesis'''
    funName = p[1]
    if funName not in context.funs:
        raise SystemExit("function '{}' does not exist at line {}".format(funName, p.lineno(1)))
    fun = context.funs[funName]
    p[0] = fun.content


@grammar
def defFun(p: YaccProduction):
    '''noLine : DefFun ID funScope OpenParenthesis arguments CloseParenthesis OpenCurlyBracket lines CloseCurlyBracket'''
    fun = boa({})
    fun.name = p[2]
    fun.args = context.funScope.args
    fun.returns = context.funScope.returns
    fun.content = p[8]

    context.clearFunScope()
    context.registerFun(fun)


@grammar
def funScope(p: YaccProduction):
    '''funScope :'''
    if context.inFunScope:
        print("function definition inside function is not handled")
        raise SystemExit()
    context.inFunScope = True


@grammar
def args(p: YaccProduction):
    '''arguments : ID'''
    arg = p[1]
    arg.scopeId = context.genId()
    context.funScope.args.append(arg)


@grammar
def args_empty(p: YaccProduction):
    '''arguments : '''


@grammar
def args_many(p: YaccProduction):
    '''arguments : arguments Comma ID'''
    arg = p[3]
    arg.scopeId = context.genId()
    context.funScope.args.append(arg)


# def genIfsLines(infoIf, infoElif, elseLines):
#     infoElif = infoElif if infoElif is not None else boa({'ifConditions': [], 'contents': []})
#     endJump = Jump('endJump', infoIf.refEndIf)
#     return [
#         infoIf.ifCondition, *infoElif.ifConditions,
#         *elseLines,
#         endJump,
#         *infoElif.contents.reduce(lambda lines, content: lines + [*content, endJump], []),
#         *infoIf.content,
#         infoIf.refEndIf,
#     ]
