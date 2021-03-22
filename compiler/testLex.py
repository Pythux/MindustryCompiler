#!/usr/bin/env python

# ------------------------------------------------------------
# tokenizer
# ------------------------------------------------------------

# import ply.lex as lex

from ply import lex


# List of token names.   This is always required
tokens = (
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',

    'Indent',
    'Word',
    'Number',
    )

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_Word = r'[a-zA-Z_]\S*'
# \S Matches anything other than a space, tab or newline.


# A regular expression rule with some action code
def t_Number(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_Indent(t):
    r'\n(\t|[ ]{4})*'
    t.value = len(t.value[1:].replace(' '*4, '\t'))
    return t


# # Define a rule so we can track line numbers
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ''


# Error handling rule
def t_error(t):
    if t.value[0] == ' ':
        t.lexer.skip(1)
    elif t.value[0] == '\n':
        t.lexer.skip(1)
    else:
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
if true jump
    yé
        yo
iftruejump
'''

# Give the lexer some input
lexer.input(data)


for tok in lexer:
    print(tok)
