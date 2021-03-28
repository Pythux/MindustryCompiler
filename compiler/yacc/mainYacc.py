
from typing import List, T


from .generateYacc import generateYaccFunctions

# import grammar
from . import grammar  # noqa


# generate module .p_functionYacc
generateYaccFunctions()


# get parser for generated file
from .p_functionYacc import parser  # noqa


# run parser on content
def runYacc(content: str):
    lines = parser.parse(content)
    stringCode = changeRefToLineNumber(lines)
    return stringCode


# we only have at this moment str or Jump Objects in lines
def changeRefToLineNumber(li: List[T]):
    lines = []
    for el in li:
        if isinstance(el, str):
            lines.append(el)
        elif isinstance(el, refJump.Jump):
            lines.append(el.toLine(refDict))
        else:
            raise Exception('wtf')
    return '\n'.join(lines) + '\n'


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
