
from compiler.yacc.grammar.jump import Jump
from ._start import grammar, YaccProduction, context


# if a < b
#     print 'a < b'
# print 'yo'
#
# jump ifCond a < b
# jump endIf
# #ref ifCond
# print 'a < b'
# #ref endIf
@grammar
def ifInstr(p: YaccProduction):
    '''lines : If asmCondition OpenCurlyBracket lines CloseCurlyBracket'''
    lines = []
    refIf, refEndIf = context.genRef(), context.genRef()
    lines.append(Jump(p.lineno, refIf, p[2]))
    lines.append(Jump(p.lineno, refEndIf))

    lineDiff = 2 - len(p[4])  # because lines couted in lines p[4]
    context.addRef(refIf, lineDiff=lineDiff)
    lines += p[4]
    context.addRef(refEndIf, lineDiff=lineDiff+len(p[4]))
    p[0] = lines
