import ply.lex as lex
import re

tokens = (
    'ID', 'STR', 'NUM', 'FLT'
)

keywords = (
    'cmd', 'fn',
    'User', 'str', 'num', 
    'const', 'mut',
    'new',
    'use', 'pkg',
    'if', 'else', 'elseif', 
    'while', 'for'
)

for kw in keywords:
    tokens += (kw,)

symbols = {
    '+': "PLUS", 
    '-': "MINUS", 
    '*': "MULTIPLY", 
    '/': "DIVIDE", 
    '%': "MODULO",
    ":": "COLON",
    "=": "EQUALS",
    "->": "ARROW",
    ",": "COMMA",
    " ()": "PAREN",
    f" {'{}'}": "BRACE", #hacky fix for lite-xl's incorrect syntax highlighter
    "::": "DOUBLECOLON",
    "==": "EQS",
    "!=": "NEQS",
    ">=": "MEQS",
    "<=": "LEQS",
    "<" : "LT",
    ">" : "MT",
}

for k,v in symbols.items():
    if len(k) != 3:
        globals()['t_' + v] = re.escape(k)
        tokens += (v,)
    else:
        cs = "LR"
        for i,c in enumerate(k.strip()):
            globals()['t_' + cs[i]+v] = re.escape(k.strip()[i])
            tokens+=(cs[i]+v,)
t_ignore = ' \t'

def t_FLT(t):
    r'(\d*\.\d+)|(\d+\.\d*)'
    t.value = float(t.value)
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STR(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in keywords:
        t.type = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'\/\/.*'


def t_error(t): pass

lexer = lex.lex()
