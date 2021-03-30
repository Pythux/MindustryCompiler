from boa import boa
from .contextAndClass import Jump
from ._start import grammar, YaccProduction, context


@grammar
def linesFromIf(p: YaccProduction):
    '''lines : ifBlock'''
    infoIf = p[1]
    p[0] = genIfsLines(infoIf, None, [])


@grammar
def linesFromIfElse(p: YaccProduction):
    '''lines : ifBlock elseBlock'''
    infoIf = p[1]
    elseLines = p[2]
    p[0] = genIfsLines(infoIf, None, elseLines)


@grammar
def linesFromIfElseElseIf(p: YaccProduction):
    '''lines : ifBlock elifs'''
    infoIf = p[1]
    infoElif = p[2]
    p[0] = genIfsLines(infoIf, infoElif, [])


@grammar
def linesFromIfElseElseIfElse(p: YaccProduction):
    '''lines : ifBlock elifs elseBlock'''
    infoIf = p[1]
    infoElif = p[2]
    elseLines = p[3]
    p[0] = genIfsLines(infoIf, infoElif, elseLines)


def genIfsLines(infoIf, infoElif, elseLines):
    infoElif = infoElif if infoElif is not None else boa({'ifConditions': [], 'contents': []})
    endJump = Jump('endJump', infoIf.refEndIf)
    return [
        infoIf.ifCondition, *infoElif.ifConditions,
        *elseLines,
        endJump,
        *infoElif.contents.reduce(lambda lines, content: lines + [*content, endJump], []),
        *infoIf.content,
        infoIf.refEndIf,
    ]


@grammar
def elifs_one(p: YaccProduction):
    '''elifs : elseIfBlock'''
    infoIf = p[1]
    info = boa({})
    info.ifConditions = [infoIf.ifCondition]
    info.contents = [infoIf.content]
    p[0] = info


@grammar
def elifs_many(p: YaccProduction):
    '''elifs : elifs elseIfBlock'''
    infoElif = p[1]
    infoIf = p[2]
    infoElif.ifConditions.append(infoIf.ifCondition)
    infoElif.contents.append(infoIf.content)
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
    info.content = [refIf, *p[4]]
    p[0] = info


@grammar
def elifBlock(p: YaccProduction):
    '''elseIfBlock : ElseIf asmCondition OpenCurlyBracket lines CloseCurlyBracket'''
    info = boa({})
    refIf = context.genRef()
    info.ifCondition = Jump('jump of elseifBlock: "{}"'.format(p[2]), refIf, p[2])
    info.refEndIf = context.genRef()
    info.content = [refIf, *p[4]]
    p[0] = info
