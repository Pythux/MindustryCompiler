#!/usr/bin/env python

# ------------------------------------------------------------
# tokenizer with Lex
# ------------------------------------------------------------

# import ply.lex as lex

from ply import lex
from ply.lex import Lexer

from boa import boa


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


# add functions that turn to tokens
tokens += [
    'Number',
    'Indent',
    'RefJump',
]


# A regular expression rule with some action code
def t_Number(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_Indent(t):
    r'\n(\t|[ ]{4})*'
    t.value = len(t.value[1:].replace(' '*4, '\t'))
    t.lexer.lineno += 1  # inc line number to track lines
    return t


def t_RefJump(t):
    r'[#][Rr]ef[:]?[ ][a-zA-Z_]\S*'
    t.value = t.value.split(' ')[-1]
    return t


reserved = {
    # new ones (or witch change)
    'if': 'If',
    'jump': 'Jump',
    'def': 'Function',
    'return': 'FunReturn',

    'not': 'NotEqual',
    'true': 'True',
    'false': 'False',
}
tokens += list(reserved.values())
tokens += ['Variable']  # not reserved words


# function starting with t_ will be run for tokens even if not in tokens list
def t_Word(t):
    r'[a-zA-Z_]\S*'  # \S Matches anything other than a space, tab or newline.
    # print(t.type) == 'Word'
    t.type = reserved.get(t.value, 'Variable')  # Check for reserved words
    return t


tokens += ['ArobasedInfo']


def t_ArobasedInfo(t):
    r'@\w+'
    return t


# must be defined before SpecialWord
# discards comments line (aka: //)
def t_Comments(t):
    r'\/\/.*'
    # no return, token discarded


# operation = {
#     '+': 'Plus',
#     '-': 'Minus',
#     '*': 'Multiply',
#     '/': 'Divide',
#     '(': 'LeftParentheses',
#     ')': 'RightParentheses',
# }
# tokens += list(operation.values())


# def t_Operation(t: LexToken):
#     r'[\+\-\*](\d|\s{1}|[\(])'  # op, number, '(' or whitespace char
#     breakpoint()
#     # return t


reservedSpecial = {
    '==': 'Equal',
    '===': 'StrictEqual',
    '!=': 'NotEqual',
    '>': 'GreaterThan',
    '>=': 'GreaterThanOrEqual',
    '<': 'LowerThan',
    '<=': 'LowerThanOrEqual',
}
tokens += (reservedSpecial.values())
startReservedSpecial = boa(list(reservedSpecial.keys())).map(lambda w: w[0])


# catch everything else that function on trop don't catch
def t_SpecialWord(t):
    r'\S+'  # \S Matches anything other than a space, tab or newline
    if t.value[0] in startReservedSpecial:
        t.type = reservedSpecial[t.value]  # Check for reserved words
        return t
    print('SpecialWord not match: {}'.format(t))


# A string containing ignored characters (spaces and tabs)
t_ignore = ''


# Error handling rule
def t_error(t):
    if t.value[0] == ' ':
        t.lexer.skip(1)
    else:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


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
