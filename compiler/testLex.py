#!/usr/bin/env python

# ------------------------------------------------------------
# tokenizer
# ------------------------------------------------------------

# import ply.lex as lex

from ply import lex


# List of token names.   This is always required
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    )


# Regular expression rules for simple tokens
t_PLUS    = r'\+'  # noqa
t_MINUS   = r'-'   # noqa
t_TIMES   = r'\*'  # noqa
t_DIVIDE  = r'/'   # noqa
t_LPAREN  = r'\('  # noqa
t_RPAREN  = r'\)'  # noqa


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
3 + 4 * 10
+ -20 *2
'''

# Give the lexer some input
lexer.input(data)


for tok in lexer:
    print(tok)
