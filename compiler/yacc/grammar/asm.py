
from ._start import grammar, YaccProduction, context
from ..classes import AsmInst, Variable, Value
from . import asmError as err


# catch all ASM as it, no processing them
# @grammar
# def lineAsm(p: YaccProduction):
#     '''line : asmInstr asmValideInstructions EndLine'''
#     p[0] = AsmInst(p[1], p[2])


@grammar
def asmInstr(p: YaccProduction):
    '''asmInstr : ID'''
    if p[1] == 'op':
        context.nextNoVar = 1
    elif p[1] == 'radar':
        context.nextNoVar = 5
    elif p[1] == 'ucontrol':
        context.nextNoVar = 1
    elif p[1] == 'ulocate':
        context.nextNoVar = 2
    p[0] = p[1]


@grammar
def resultOpTwoArgs(p: YaccProduction):
    '''line : op opTwoArgs ID info info EndLine'''
    breakpoint()


@grammar
def instrError(p: YaccProduction):
    '''line : info error'''
    raise err.invalideInstr(p, line=p.lineno(2))


@grammar
def instrKeyErrorError(p: YaccProduction):
    '''line : error'''
    raise err.invalideInstr(p, line=p.lineno(1))


@grammar
def instrKeywordOp_error(p: YaccProduction):
    '''line : op error'''
    raise err.invalideSubInstr(p)


@grammar
def opTwoArgsResult_error(p: YaccProduction):
    '''line : op opTwoArgs error'''
    raise err.mustBeVar(p, 3)


@grammar
def opTwoArgsArgs_error(p: YaccProduction):
    '''line : op opTwoArgs ID error
            | op opTwoArgs ID info error'''
    givenArgs = len(p) - 5
    raise err.maybeNotEnoughtArgs(p, 2, givenArgs)


@grammar
def opTwoArgsArgsTooMuch_error(p: YaccProduction):
    '''line : op opTwoArgs ID info info error'''
    raise err.tooManyArgs(p, 2)


@grammar
def opTwoArgs(p: YaccProduction):
    '''opTwoArgs : add'''
    pass


@grammar
def asmFollowInstructions_one(p: YaccProduction):
    '''asmValideInstructions : info'''
    p[0] = [p[1]]


@grammar
def asmFollowInstructions_many(p: YaccProduction):
    '''asmValideInstructions : asmValideInstructions info'''
    p[0] = p[1] + [p[2]]


@grammar
def info_id(p: YaccProduction):
    '''info : ID'''
    info = Variable(p[1])
    if context.nextNoVar > 0:
        context.nextNoVar -= 1
    elif context.fun.inFunScope:
        p[0] = context.fun.scopeId(info)
        return

    p[0] = info


@grammar
def info(p: YaccProduction):
    '''info : Number
            | String
            | ArobasedInfo
            | True
            | False
    '''
    p[0] = Value(p[1])
