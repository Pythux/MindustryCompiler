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
    r'".*"'
    t.type = 'String'
    return t


def t_stringSimpleQuote(t: LexToken):
    r"'.*'"
    t.type = 'String'
    return t


# count indentation, 4 saces or 1 tab = 1 lvl of indent
def t_EndLine(t: LexToken):
    r'\n'
    t.lexer.lineno += 1  # inc line number to track lines
    return t


# match: '#ref st', '#Ref st', '#ref: st', '#Ref: st', '#ref é4sét$sr'
def t_RefJump(t: LexToken):
    r'[#][Rr]ef[:]?[ ]\S*'
    t.value = t.value.split(' ')[-1]
    return t


# reserved keyword
reserved = {
    'jump': 'Jump',
}
tokens += list(reserved.values())
tokens += ['ID']  # not reserved words


# function starting with t_ will be run for tokens even if not in tokens list
def t_Word(t: LexToken):
    r'[a-zA-Z_]\S*'  # \S Matches anything other than a space, tab or newline.
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
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
    '==': ['equal', 'notEqual'],
    # '===': ['StrictEqual', 'strictEqual'],
    '!=': ['notEqual', 'equal'],
    '>': ['greaterThan', 'lessThanEq'],
    '>=': ['greaterThanEq', 'lessThan'],
    '<': ['lessThan', 'greaterThanEq'],
    '<=': ['lessThanEq', 'greaterThan'],
}
tokens += ['Comparison']


# catch everything else that function on trop don't catch
def t_SpecialWord(t: LexToken):
    r'\S+'  # \S Matches anything other than a space, tab or newline

    if t.value[0] == '#':
        return None  # comments "#"

    if t.value in comparison:
        t.type = 'Comparison'
        t.value = comparison[t.value]
        return t

    print('SpecialWord not match: {}'.format(t))
    print("line: {}".format(t.lineno))
    raise SystemExit()


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
    for tok in lexer:
        print(tok)


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

        runLex(content)
        content = ''
