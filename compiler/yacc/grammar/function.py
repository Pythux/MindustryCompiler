
from compiler import CompilationException
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
    '''ligne : affectation dottedID OpenParenthesis arguments CloseParenthesis'''
    returnTo = p[1]
    dotted = p[2]
    module, funName = getModuleAndFunName(dotted)
    callArgs = p[4]
    p[0] = FunCall(module, funName, callArgs, p.lineno(3), returnTo)


@grammar
def runFunc(p: YaccProduction):
    '''ligne : dottedID OpenParenthesis arguments CloseParenthesis'''
    dotted = p[1]
    module, funName = getModuleAndFunName(dotted)
    callArgs = p[3]
    p[0] = FunCall(module, funName, callArgs, p.lineno(2))


@grammar
def defFun(p: YaccProduction):
    '''noLine : dottedID OpenParenthesis arguments CloseParenthesis OpenCurlyBracket lines CloseCurlyBracket''' # noqa
    if len(p[1]) != 1:
        raise CompilationException("function definition incorrect: {} is not accepted".format(p[1]))
    funName = p[1][0]
    args = p[3]
    content = p[6]
    importsHandling.imports.addFunToModule(context.getDefinedFunction())


@grammar
def funContent(p: YaccProduction):
    '''funContent : ligne
                  | lignes
                  | returnStatement
                  | ligne returnStatement'''
    breakpoint()


# # register function definition arguments
# def addArguments(args):
#     for arg in args:
#         if arg in context.fun.args:
#             raise CompilationException('Duplicate parameter "{}"'.format(arg))
#         context.fun.args.append(arg)
#         context.fun.scopeId(arg)


@grammar
def handleReturn(p: YaccProduction):
    '''returnStatement : Return arguments'''
    p[p] = p[2]
    return
    if not context.fun.inFunScope:
        raise CompilationException("return keyword only indide function definition, line {}".format(p.lineno(1)))
    p[0] = funReturn(p[2])


def funReturn(args):
    if context.fun.returns is None:
        # no return meet before
        context.fun.returns = [context.fun.genId() for _ in range(len(args))]

    # exact same return quantity
    if len(args) != len(context.fun.returns):
        raise CompilationException("function {} must return {} as many values for all it's return"
                                   .format(context.fun.name, len(context.fun.returns)))

    lines = setters(context.fun.returns, args)
    lines.append(Jump('return', context.fun.returnRef))
    return lines


# set {liSet} {liVal}
def setters(liSet, liVar):
    return [AsmInst('set', [s, v]) for s, v in zip(liSet, liVar)]
