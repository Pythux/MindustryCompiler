
from compiler.lex.mainLex import runLex
from typing import List, T
from boa import boa

from . import importsHandling


from .generateYacc import generateYaccFunctions

# import grammar, required
from . import grammar  # noqa

from .context import context
from .classes import Jump, Ref, FunCall, AsmInst, Variable


# generate module .p_functionYacc
generateYaccFunctions()


# get parser for generated file
from .p_functionYacc import parser  # noqa


def yaccParse(content, debug=False):
    if not len(content):
        return ''
    if content[-1] != '\n':
        content += '\n'
    lines = parser.parse(content, debug=debug)
    return lines


# run parser on content, which is main file or REPL
def runYacc(content: str, debug=False, clearContext=False):
    checkExistingVars(content)  # only on main file
    lines = yaccParse(content, debug=debug)

    runImports()
    # back to main file:
    if lines is None or len(lines) == 0:
        return ''

    lines = fillFunCall(lines)

    # last step, put ref to code line
    lines = consumeRefAndChangeJump(lines)

    stringLi = boa(lines).map(lambda line: line.toStr())

    stringCode = '\n'.join(stringLi) + '\n'

    if clearContext:
        importsHandling.imports.clear()
        context.clear()
    return stringCode


# run all imports to do
def runImports():
    for nextImpContent in importsHandling.nextImportContent():
        yaccParse(nextImpContent)


def fillFunCall(lines):
    lines = boa(lines)
    if len(lines.filter(lambda el: isinstance(el, FunCall))) == 0:
        return lines

    def reducer(li, el):
        return li + (el.toContent() if isinstance(el, FunCall) else [el])

    return fillFunCall(lines.reduce(reducer, []))


def checkExistingVars(content):
    context.existingVars = set((
        boa(runLex(content))
        .filter(lambda tok: tok.type == 'ID')
        .map(lambda tok: Variable(tok.value))))


# we only have at this moment str, Jump and Ref Objects in lines
def consumeRefAndChangeJump(li: List[T]):
    if isinstance(li[-1], Ref):
        li.append(AsmInst('end', []))  # finish with end statement to #ref on it

    li = consumeRef(li)  # build refDictionary

    # change jump ref to jump lineNumb
    for el in li:
        if isinstance(el, Jump):
            el.refToLine(context.refDict)

    return li


def consumeRef(li: List[T]):
    result = []
    for el in li:
        if isinstance(el, Ref):
            context.addRef(el, len(result))
        else:
            result.append(el)
    return result


def runInteractiveYacc():
    content = ''
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        if s:
            content += s + '\n'
            continue
        if content == '':
            continue
        print(runYacc(content))
        content = ''
