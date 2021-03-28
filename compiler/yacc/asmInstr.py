
# from .yaccImport import YaccProduction

from .generateYacc import grammar


@grammar
def p_asmLine(p):
    '''asmInstr : asmValideInstructions EndLine'''
    p[0] = p[1]



# # to keep the "valide ASM will pass"
# def p_jump_asmNoRef(p: YaccProduction):
#     '''asmInstr : Jump Number asmCondition EndLine'''
#     p[0] = p[1] + ' ' + str(p[2]) + ' ' + p[3]


# # catch all ASM as it, no processing them
# def p_asmLine(p: YaccProduction):
#     '''asmInstr : asmValideInstructions EndLine'''
#     p[0] = p[1]


# def p_asmFollowInstructions_one(p: YaccProduction):
#     '''asmValideInstructions : info'''
#     p[0] = str(p[1])


# def p_asmFollowInstructions_many(p: YaccProduction):
#     '''asmValideInstructions : asmValideInstructions info'''
#     p[0] = p[1] + ' ' + str(p[2])
