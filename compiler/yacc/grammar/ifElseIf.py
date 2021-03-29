from boa import boa
from .contextAndClass import Jump, Ref
from ._start import grammar, YaccProduction, context


@grammar
def linesFromIfElse(p: YaccProduction):
    '''lines : ifBlock
             | ifElse'''


@grammar
def ifElse(p: YaccProduction):
    '''ifElse : ifBlock elseBlock'''
    info = p[1]
    info.ifCondition
    info.ifContent
    elseContent = p[2]
    return [
        info.ifCondition, *info.ifContent,
        *elseContent, Jump(p.lineno, info.refEndIf),
        info.refEndIf]


@grammar
def linesFromIfElseElseIf(p: YaccProduction):
    '''lines : ifElseElseIf'''


@grammar
def ifElseElseIf(p: YaccProduction):
    '''ifElseElseIf : ifBlock elifs elseBlock'''
    print('else')
    breakpoint()


@grammar
def elifs_one(p: YaccProduction):
    '''elifs : elseIfBlock'''


@grammar
def elifs_many(p: YaccProduction):
    '''elifs : elifs elseIfBlock'''


@grammar
def elseIfBlock(p: YaccProduction):
    '''elseIfBlock : Else ifBlock'''


@grammar
def elseInstr(p: YaccProduction):
    '''elseBlock : Else OpenCurlyBracket lines CloseCurlyBracket'''
    p[0] = p[3]  # lines


# if a < b
#     print 'a < b'
# else:
#     print 'a >= b'
# print 'yo'
#
# jump ifCond a < b
# print 'a >= b'
# jump endIf
# #ref ifCond
# print 'a < b'
# #ref endIf


@grammar
def ifBlock(p: YaccProduction):
    '''ifBlock : If asmCondition OpenCurlyBracket lines CloseCurlyBracket'''
    info = boa({})
    refIf = context.genRef()
    info.ifCondition = Jump(p.lineno, refIf, p[2])
    info.refEndIf = context.genRef()
    info.ifContent = p[4].append(Jump(p.lineno, info.refEndIf))
    p[0] = info
