

from compiler.yacc.classes.AsmInst import Variable
from ._start import grammar, YaccProduction, context
from boa import boa
from ..classes import Ref, Jump


# ressourceList = [(1, cuivre, @copper), (2, plomb, @lead)]
# for id, ressource, ressourceType in ressourceList
#     if toTakeId == id

# it's call will be replaced with the value given
# there is no scope for macro, that is the big difference with fuctions
@grammar
def staticFor(p: YaccProduction):
    '''lines : For arguments ID liNameOrList OpenCurlyBracket lines CloseCurlyBracket'''
    decompose = p[2]
    li = p[4]
    originalLines = p[6]

    refDict = {}

    # create list of ref
    for line in originalLines:
        if isinstance(line, Ref):
            refDict[line] = None

    for el in li:
        if len(decompose) != len(el):
            raise Exception("cannot unpack list, el length not equal")
    # do a variable replacing
    lines = []

    for tuple in li:
        copiedLines = [el.copy() for el in originalLines]
        for k in refDict.keys():  # new refs
            refDict[k] = context.genRef()
        for line in copiedLines:
            if isinstance(line, Ref):  # change ref
                line.changeRef(refDict[line])
            elif isinstance(line, Jump):
                if line.ref in refDict:
                    line.changeRef(refDict[line.ref])
                for toReplace, toReplaceBy in zip(decompose, tuple):
                    line.replace(toReplace, toReplaceBy)
            else:
                for toReplace, toReplaceBy in zip(decompose, tuple):
                    line.replace(toReplace, toReplaceBy)
        lines += copiedLines
    p[0] = lines


@grammar
def liNameOrList(p: YaccProduction):
    '''liNameOrList : ID
                    | list'''
    liNameOrList = p[1]
    p[0] = liNameOrList if isinstance(liNameOrList, list) else context.staticVarsList[Variable(liNameOrList)]


@grammar
def staticList(p: YaccProduction):
    '''noLine : affectation list'''
    if len(p[1]) != 1:
        raise Exception("afectation incorrect: {} is not accepted".format(p[1]))
    name = p[1][0]
    val = p[2]
    if name in context.staticVarsList:
        raise Exception("static list named: ⸄{}⸅ alrealy defined".format(name))
    context.staticVarsList[name] = val


@grammar
def staticList_list(p: YaccProduction):
    '''list : OpenBracket tuplesOrInfo CloseBracket'''
    p[0] = p[2]


@grammar
def tuplesOrInfo(p: YaccProduction):
    '''tuplesOrInfo : tuples
                    | arguments'''
    val = p[1]
    if isinstance(val[0], list):
        p[0] = p[1]
    else:
        p[0] = boa(val).map(lambda el: [el])


@grammar
def tuples_one(p: YaccProduction):
    '''tuples : tuple'''
    p[0] = [p[1]]


@grammar
def tuples_many(p: YaccProduction):
    '''tuples : tuples Comma tuple'''
    p[0] = p[1] + [p[3]]


@grammar
def tuples_oneComma(p: YaccProduction):
    '''tuples : tuples Comma'''
    p[0] = p[1]



@grammar
def tupleDef(p: YaccProduction):
    '''tuple : OpenParenthesis arguments CloseParenthesis'''
    p[0] = p[2]
