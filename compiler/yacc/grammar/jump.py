
from ._start import grammar, YaccProduction, context

from .contextAndClass import Jump, Ref


# handle a ref instruction, we store info in context.refDict and discard information
@grammar
def ref(p: YaccProduction):
    '''line : RefJump EndLine'''
    ref = p[1]
    if context.fun.inFunScope:
        ref = context.fun.scopeRef(ref)

    p[0] = Ref(ref)


# a line is ether a jump instruction or an asmInstr
@grammar
def lineJump(p: YaccProduction):
    '''line : jump'''
    p[0] = p[1]


@grammar
def jump_asmCondition(p: YaccProduction):
    '''jump : Jump ID asmCondition EndLine'''
    # get for error message line of jump instruction
    ref = p[2]
    if context.fun.inFunScope:
        ref = context.fun.scopeRef(ref)
    jump = Jump(p.lineno(1), Ref(ref), p[3])
    p[0] = jump


@grammar
def comparison(p: YaccProduction):
    '''asmCondition : info Comparison info'''
    p[0] = p[2] + ' ' + str(p[1]) + ' ' + str(p[3])


@grammar
def jump_always(p: YaccProduction):
    '''jump : Jump ID EndLine'''
    ref = p[2]
    if context.fun.inFunScope:
        ref = context.fun.scopeRef(ref)
    p[0] = Jump(p.lineno(1), Ref(ref))


# to keep the "valide ASM will pass"
@grammar
def jump_asmNoRef(p: YaccProduction):
    '''line : Jump Number asmCondition EndLine'''
    p[0] = p[1] + ' ' + str(p[2]) + ' ' + p[3]


@grammar
def asmCondition(p: YaccProduction):
    '''asmCondition : ID info info'''
    p[0] = p[1] + ' ' + str(p[2]) + ' ' + str(p[3])
