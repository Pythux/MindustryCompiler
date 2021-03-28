
from ._start import grammar, YaccProduction, context


# handle a ref instruction, we store info in context.refDict and discard information
@grammar
def ref(p: YaccProduction):
    '''noLine : RefJump EndLine'''
    ref = p[1]
    context.addRef(ref)


class Jump:
    def __init__(self, line, ref, condition=None) -> None:
        self.line = line
        self.ref = ref
        self.asmCondition = condition if condition is not None else 'always true true'

    def toLine(self):
        if self.ref not in context.refDict:
            print("for jump at line: {}".format(self.line))
            print("ref {} not exist, existing ref: {}".format(self.ref, context.refDict))
            raise SystemExit()
        return 'jump {ref} {condition}'.format(
            ref=context.refDict[self.ref], condition=self.asmCondition)


@grammar
def jump_asmCondition(p: YaccProduction):
    '''jump : Jump ID asmCondition EndLine'''
    # get for error message line of jump instruction
    jump = Jump(p.lineno(1), p[2], p[3])
    p[0] = jump


@grammar
def comparison(p: YaccProduction):
    '''asmCondition : info Comparison info'''
    p[0] = p[2] + ' ' + str(p[1]) + ' ' + str(p[3])


@grammar
def jump_always(p: YaccProduction):
    '''jump : Jump ID EndLine'''
    p[0] = Jump(p.lineno(1), p[2])


# to keep the "valide ASM will pass"
@grammar
def jump_asmNoRef(p: YaccProduction):
    '''asmInstr : Jump Number asmCondition EndLine'''
    p[0] = p[1] + ' ' + str(p[2]) + ' ' + p[3]


@grammar
def asmCondition(p: YaccProduction):
    '''asmCondition : ID info info'''
    p[0] = p[1] + ' ' + str(p[2]) + ' ' + str(p[3])
