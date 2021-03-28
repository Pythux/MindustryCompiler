
from typing import Callable, List, T
from .yaccImport import yacc, YaccProduction


# Get the token map from the lexer.  This is required.
from compiler.lex import tokens, lexer  # noqa
from compiler.lex.mainLex import LexToken


from .yaccRules import parser


# Build the parser
def buildParser():
    parser = yacc.yacc()
    return parser


# read file given
def runYacc(content: str, keepData=False):
    lines = parser.parse(content)
    stringCode = changeRefToLineNumber(lines)
    if not keepData:
        clearData()
    return stringCode


def clearData():
    global lineNumber, refDict
    lineNumber = 0
    refDict = {}


# we only have at this moment string or Jump Objects in lines
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
        print(runYacc(content, keepData=True))
        content = ''
