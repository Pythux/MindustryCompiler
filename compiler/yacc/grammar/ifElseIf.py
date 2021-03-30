from boa import boa
from .contextAndClass import Jump
from ._start import grammar, YaccProduction, context


@grammar
def linesFromIf(p: YaccProduction):
    '''lines : ifBlock'''
    info = p[1]
    p[0] = [
        info.ifCondition,
        Jump(p.lineno, info.refEndIf),
        *info.ifContent,
        info.refEndIf]


@grammar
def linesFromIfElse(p: YaccProduction):
    '''lines : ifBlock elseBlock'''
    info = p[1]
    elseContent = p[2]
    p[0] = [
        info.ifCondition, *elseContent, Jump(p.lineno, info.refEndIf),
        *info.ifContent,
        info.refEndIf]


@grammar
def linesFromIfElseElseIf(p: YaccProduction):
    '''lines : ifBlock elifs elseBlock'''
    infoIf = p[1]
    infoElif = p[2]
    elseLines = p[3]
    endJump = Jump('gen', infoIf.refEndIf)
    result = [
        infoIf.ifCondition, *infoElif.ifConditions,
        *elseLines,
        endJump,
        *infoElif.contents.reduce(lambda lines, content: lines + [*content, endJump], []),
        *infoIf.ifContent,
        infoIf.refEndIf,
    ]
    p[0] = result


@grammar
def elifs_one(p: YaccProduction):
    '''elifs : elseIfBlock'''
    infoIf = p[1]
    info = boa({})
    info.ifConditions = [infoIf.ifCondition]
    info.contents = [infoIf.ifContent]
    p[0] = info


@grammar
def elifs_many(p: YaccProduction):
    '''elifs : elifs elseIfBlock'''
    infoElif = p[1]
    infoIf = p[2]
    infoElif.ifConditions.append(infoIf.ifCondition)
    infoElif.contents.append(infoIf.ifContent)
    p[0] = infoElif


@grammar
def elseIfBlock(p: YaccProduction):
    '''elseIfBlock : Else ifBlock'''
    infoIf = p[2]
    p[0] = infoIf


@grammar
def elseInstr(p: YaccProduction):
    '''elseBlock : Else OpenCurlyBracket lines CloseCurlyBracket'''
    p[0] = p[3]  # lines


@grammar
def ifBlock(p: YaccProduction):
    '''ifBlock : If asmCondition OpenCurlyBracket lines CloseCurlyBracket'''
    info = boa({})
    refIf = context.genRef()
    info.ifCondition = Jump('jump of ifBlock: "{}"'.format(p[2]), refIf, p[2])
    info.refEndIf = context.genRef()
    info.ifContent = [refIf, *p[4]]
    p[0] = info
