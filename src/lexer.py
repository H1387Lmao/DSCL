import ply.lex as lex
import re
from .hlog import *
from .errors import *
import sys

tokens = (
    'ID', 'STR', 'NUM', 'FLT'
)

keywords = (
    'cmd', 'fn', 
    'async', 'await',
    'User', 'String', 'Number', 'Context',
    'const', 'mut',
    'new',
    'use', 'pkg',
    'if', 'else', 'elseif', 
    'while', 'for', 'to', 'in'  
)

macros = {
    "ctx": "this"
}

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
    " []":"BRACKET",
    "::": "DOUBLECOLON",
    "==": "EQS",
    "!=": "NEQS",
    ">=": "MEQS",
    "<=": "LEQS",
    "<" : "LT",
    ">" : "MT",
    "." : "DOT",
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
    if t.value in macros:
        t.value = macros[t.value]
        return t
    if t.value in keywords:
        t.type = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'\/\/.*'

LexerLogger=Logger("Tokenizing")

def t_error(t):
    LexerError(LexerLogger, f"Unexpected character: '{t.value.replace('\n','')}'", t.lineno, t.lexpos)
    LexerLogger.exit_stage()

lexer = lex.lex()
