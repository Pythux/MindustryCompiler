
from compiler import CompilationException
from ._start import grammar, YaccProduction, context

from .. import importsHandling
from ..classes import AsmInst, FunDef, ReturnStm, FunCall


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
    '''noLine : dottedID OpenParenthesis arguments CloseParenthesis OpenCurlyBracket funDefContext lines CloseCurlyBracket''' # noqa
    if len(p[1]) != 1:
        raise CompilationException(
            "line {}, function definition incorrect: {} is not accepted"
            .format(p.lineno(2), p[1]))
    name = p[1][0]
    args = p[3]
    content = p[7]
    fundef = FunDef(context, name, args, content)
    importsHandling.imports.addFunToModule(fundef)
    context.inFunDefinition = False


@grammar
def funDefContext(p: YaccProduction):
    '''funDefContext : '''
    context.inFunDefinition = True


@grammar
def handleReturn(p: YaccProduction):
    '''ligne : Return arguments'''
    if not context.inFunDefinition:
        raise CompilationException(
            "line {}, return statement must be in function definition".format(p.lineno(1)))
    p[0] = ReturnStm(p[2])


# set {liSet} {liVal}
def setters(liSet, liVar):
    return [AsmInst('set', [s, v]) for s, v in zip(liSet, liVar)]
