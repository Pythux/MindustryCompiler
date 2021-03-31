#!/usr/bin/env python

# ------------------------------------------------------------
# tokenizer with Lex
# ------------------------------------------------------------

# import ply.lex as lex

from ply import lex
from ply.lex import Lexer


class LexToken:
    lexer: Lexer
    lineno: int  # will be updated by lexer
    type: str  # Token name
    value: str  # matched content, can be changed to anything


# List of token names.   This is always required
tokens = [
    # 'Plus',
]

# Regular expression rules for simple tokens
# will be check last (after functions)
# t_Plus = r'\+'


# add tokens from functions
tokens += [
    'Number',
    'ArobasedInfo',
    'String',
    'EndLine',
    'RefJump',
]


# catch numbers like 0, 1, -2, -26.465
def t_Number(t):
    r'[-]?\d+[.]?\d*'
    return t


def t_ArobasedInfo(t):
    r'@\w+'
    return t


def t_stringDoubleQuote(t: LexToken):
    r'"[^"]*"'
    t.type = 'String'
    return t


def t_stringSimpleQuote(t: LexToken):
    r"'[^']*'"
    t.type = 'String'
    return t


previousIndentationLvl = 0
indentSpacing = None
tokens += ['OpenCurlyBracket', 'CloseCurlyBracket']
addCloseBracket = False


# count indentation, 4 saces or 1 tab = 1 lvl of indent
def t_EndLine(t: LexToken):
    r'\n[ ]*'
    global previousIndentationLvl, indentSpacing, addCloseBracket
    if addCloseBracket:
        addCloseBracket = False
        t.type = 'CloseCurlyBracket'
        return t

    if indentSpacing is None:
        spaces = len(t.value[1:])
        if spaces > 0:
            indentSpacing = spaces
    indent = len(t.value[1:])
    if indentSpacing:
        indent = len(t.value[1:].replace(' '*indentSpacing, '\t'))
    if indent > previousIndentationLvl:
        t.type = 'OpenCurlyBracket'
    elif indent < previousIndentationLvl:
        t.type = 'EndLine'
        addCloseBracket = True
        t.lexer.lexpos -= len(t.value)
    previousIndentationLvl = indent
    t.lexer.lineno += 1  # inc line number to track lines
    return t


# match: '#ref st', '#Ref st', '#ref: st', '#Ref: st', '#ref é4sét$sr'
def t_RefJump(t: LexToken):
    r'[#][Rr]ef[:]?[ ][^0-9]\S*'
    t.value = t.value.split(' ')[-1]
    return t


# discards comments line (aka: '//')
# must be defined before SpecialWord to catch it
def t_CommentsSlashSlash(t):
    r'\/\/.*'
    # no return, token discarded


# discards comments line (aka: '# ')
def t_CommentsHashSpace(t):
    r'[#][ ].*'
    # no return, token discarded


comparison = {
    '==': 'equal',
    '===': 'strictEqual',
    '!=': 'notEqual',
    '>': 'greaterThan',
    '>=': 'greaterThanEq',
    '<': 'lessThan',
    '<=': 'lessThanEq',
}
tokens += ['Comparison']


def t_Comparison(t: LexToken):
    r'[=!<>]+'
    if t.value in comparison:
        t.type = 'Comparison'
        t.value = comparison[t.value]
        return t


# reserved keyword
reserved = {
    'jump': 'Jump',
    'if': 'If',
    'else': 'Else',
    'elif': 'ElseIf',
    'def': 'DefFun',
    'return': 'Return',
}
tokens += list(reserved.values())
tokens += ['ID']  # not reserved words


# function starting with t_ will be run for tokens even if not in tokens list
def t_Word(t: LexToken):
    r'''[^ \n.,()*{}'"]+'''
    # r'''[^ .,()'"*{}\n]+'''  # match words, including utf-8 characters
    if t.value[0] == '#':
        return None  # unofficial comments "#"

    t.type = reserved.get(t.value, 'ID')  # Check for reserved word, else ID
    return t


separator = {
    '(': 'OpenParenthesis',
    ')': 'CloseParenthesis',
    ',': 'Comma',
}
tokens += list(separator.values())


def t_Separator(t: LexToken):
    r'''[.,()*{}]'''
    t.type = separator[t.value]
    return t


def t_Space(t: LexToken):
    '''[ ]'''


# A string containing ignored characters, could be (spaces and tabs)
t_ignore = '\r'


# Error handling rule
def t_error(t: LexToken):
    if t.value[0] == ' ':
        t.lexer.skip(1)
    else:
        print("Illegal character '%s'" % t.value[0])
        print("line: {}".format(t.lineno))
        raise SystemExit()


# make a list of unique tokens
tokens = list(set(tokens))
# Build the lexer
lexer = lex.lex()
# debugging:
# lexer = lex.lex(debug=True)


def runLex(content):
    lexer.input(content)
    li = [tok for tok in lexer]
    lexer.lineno = 1
    return li


def runInteractiveLex():
    content = ''
    while True:
        try:
            s = input('Lex >> ')
        except EOFError:
            break
        if s != '':
            content += s + '\n'
            continue

        print(runLex(content))
        content = ''
