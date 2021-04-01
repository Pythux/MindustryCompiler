
from ._start import grammar, YaccProduction, context


# catch all ASM as it, no processing them
@grammar
def lineAsm(p: YaccProduction):
    '''line : asmInstr asmValideInstructions EndLine'''
    p[0] = p[1] + ' ' + p[2]


@grammar
def asmInstr(p: YaccProduction):
    '''asmInstr : ID'''
    if p[1] == 'op':
        context.nextNoVar = 1
    elif p[1] == 'radar':
        context.nextNoVar = 5
    elif p[1] == 'ucontrol':
        context.nextNoVar = 1
    p[0] = p[1]


@grammar
def lineEnd(p: YaccProduction):
    '''line : ID EndLine'''
    if (p[1] != 'end'):
        raise SystemExit('instruction "{}" is not "end" and alone'.format(p[1]))
    p[0] = p[1]


@grammar
def asmFollowInstructions_one(p: YaccProduction):
    '''asmValideInstructions : info'''
    p[0] = str(p[1])


@grammar
def asmFollowInstructions_many(p: YaccProduction):
    '''asmValideInstructions : asmValideInstructions info'''
    p[0] = p[1] + ' ' + str(p[2])


@grammar
def info_id(p: YaccProduction):
    '''info : ID'''
    info = p[1]
    if context.nextNoVar > 0:
        context.nextNoVar -= 1
    elif context.fun.inFunScope:
        info = context.fun.scopeId(info)
    p[0] = info


@grammar
def info(p: YaccProduction):
    '''info : Number
            | String
            | ArobasedInfo
    '''
    p[0] = p[1]
