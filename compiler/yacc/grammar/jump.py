

from ._start import grammar, YaccProduction, context
from ..classes import Jump, Ref, AsmInst, Value, Comparison, KeyWord


# handle a ref instruction, we store info in context.refDict and discard information
@grammar
def ref(p: YaccProduction):
    '''ligne : RefJump EndLine'''
    ref = p[1]
    p[0] = Ref(ref)


@grammar
def jump_asmCondition(p: YaccProduction):
    '''ligne : jump ID asmCondition EndLine'''
    # get for error message line of jump instruction
    ref = p[2]
    jump = Jump(p.lineno(1), Ref(ref), p[3])
    p[0] = jump


@grammar
def comparison(p: YaccProduction):
    '''asmCondition : info Comparison info'''
    p[0] = Comparison(p[1], p[2], p[3])


@grammar
def jump_always(p: YaccProduction):
    '''ligne : jump ID EndLine'''
    ref = p[2]
    p[0] = Jump(p.lineno(1), Ref(ref))


# to keep the "valide ASM will pass"
@grammar
def jump_asmNoRef(p: YaccProduction):
    '''ligne : jump Number asmCondition EndLine'''
    instr = 'jump'
    comparison = p[3]
    liValVar = [Value(p[2]), comparison.comp, comparison.ab[0], comparison.ab[1]]
    p[0] = AsmInst(instr, liValVar)


@grammar
def asmCondition(p: YaccProduction):
    '''asmCondition : jumpKeyWord info info'''
    p[0] = Comparison(p[2], p[1], p[3])
    # it's an operation "equal, notEqual, ..., not a variable"


@grammar
def jumpKeyWord(p: YaccProduction):
    '''jumpKeyWord : equal
                   | notEqual
                   | lessThan
                   | lessThanEq
                   | greaterThan
                   | greaterThanEq
                   | strictEqual
                   | always
    '''
    p[0] = KeyWord(p[1])
