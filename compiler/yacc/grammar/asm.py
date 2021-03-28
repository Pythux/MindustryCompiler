
from ._start import grammar, YaccProduction


# catch all ASM as it, no processing them
@grammar
def asmLine(p: YaccProduction):
    '''asmInstr : asmValideInstructions EndLine'''
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
def info(p: YaccProduction):
    '''info : ID
            | Number
            | String
            | ArobasedInfo
    '''
    p[0] = p[1]
