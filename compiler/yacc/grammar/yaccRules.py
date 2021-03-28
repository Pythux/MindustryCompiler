

from ._start import grammar, YaccProduction, LexToken


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


# discard empty lines
@grammar
def noLine(p):
    '''noLine : EndLine'''


@grammar
def info(p: YaccProduction):
    '''info : ID
            | Number
            | String
            | ArobasedInfo
    '''
    p[0] = p[1]


# Error rule for syntax errors
@grammar
def error(t: LexToken):
    print("Syntax error in input!")
    print("at line: {}, wasn't expecting: {}".format(t.lineno, t.type))
    print("for more information, it's value is: {}".format(t.value))
    raise SystemExit()


# parser = yacc.yacc()
