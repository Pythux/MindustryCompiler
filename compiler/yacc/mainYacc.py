
from compiler.lex.mainLex import runLex
from typing import List, T
from boa import boa

from . import importsHandling


from .generateYacc import generateYaccFunctions

# import grammar, required
from . import grammar  # noqa

from .context import context
from .classes import Jump, Ref, FunCall


# generate module .p_functionYacc
generateYaccFunctions()


# get parser for generated file
from .p_functionYacc import parser  # noqa


def yaccParse(content, debug=False):
    if not len(content):
        return ''
    if content[-1] != '\n':
        content += '\n'
    checkExistingVars(content)
    lines = parser.parse(content, debug=debug)
    return lines


# run parser on content
def runYacc(content: str, debug=False, clearContext=False):
    lines = yaccParse(content, debug=debug)

    runImports()
    # back to main file:
    lines = fillFunCall(lines)

    # last step, put ref to code line
    stringCode = refToCodeLine(lines)

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
        return li + (el.toFunContent() if isinstance(el, FunCall) else [el])

    return fillFunCall(lines.reduce(reducer, []))


def refToCodeLine(lines):
    if len(lines) > 0:
        return changeRefToLineNumber(lines)
    return ''


def checkExistingVars(content):
    context.ids = (
        boa(runLex(content))
        .filter(lambda tok: tok.type == 'ID')
        .map(lambda tok: tok.value))


# we only have at this moment str, Jump and Ref Objects in lines
def changeRefToLineNumber(li: List[T]):
    if isinstance(li[-1], Ref):
        li.append('end')  # finish with end statement to #ref on it

    li = refToLinesNumber(li)  # change ref to lineNumb

    # change jump ref to jump lineNumb
    li = boa(li).map(lambda el: el.toLine(context) if isinstance(el, Jump) else el)
    return '\n'.join(li) + '\n'


def refToLinesNumber(li: List[T]):
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
