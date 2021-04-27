
from compiler import CompilationException
from ._start import grammar, YaccProduction, context
from ..classes import AsmInst, Variable, Value


# catch all ASM as it, no processing them
@grammar
def lineAsm(p: YaccProduction):
    '''line : asmInstr asmValideInstructions EndLine'''
    p[0] = AsmInst(p[1], p[2])


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
def lineEnd(p: YaccProduction):
    '''line : ID EndLine'''
    if (p[1] != 'end'):
        raise CompilationException('instruction "{}" is not "end" and alone'.format(p[1]))
    p[0] = AsmInst(p[1], [])


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
