
from typing import List, T
from boa import boa


from .generateYacc import generateYaccFunctions

# import grammar
from . import grammar  # noqa

from .grammar.jump import Jump, Ref
from .grammar.context import context


# generate module .p_functionYacc
generateYaccFunctions()


# get parser for generated file
from .p_functionYacc import parser  # noqa


# run parser on content
def runYacc(content: str, clearContext=False):
    lines = parser.parse(content)
    stringCode = changeRefToLineNumber(lines)
    if clearContext:
        context.clear()
    return stringCode


# we only have at this moment str, Jump and Ref Objects in lines
def changeRefToLineNumber(li: List[T]):
    if isinstance(li[-1], Ref):
        li.append('end')  # finish with end statement to #ref on it

    li = refToLinesNumber(li)  # change ref to lineNumb

    # change jump ref to jump lineNumb
    boa(li).map(lambda el: el.toLine() if isinstance(el, Jump) else el)
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
