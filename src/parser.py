import ply.yacc as yacc
from .lexer import *

# =====================
# AST CLASS
# =====================
class Ast:
    def __init__(self, n, **args):
        self.n = n
        for k, v in args.items():
            setattr(self, k, v)
    def __repr__(self):
        return repr(self.__dict__)

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
)

def p_prog(p):
    """
    prog : stmts
    """
    p[0] = Ast('prog', stmt=p[1])

def p_cmd_def(p):
    """
    stmt : cmd ID LPAREN params RPAREN scope
    """
    p[0] = Ast('cmd_decl', name=p[2], args=p[4], stmts=p[6])

def p_call(p):
    """
    stmt : ID LPAREN args RPAREN
    """
    p[0] = Ast('call', name=p[1], args=p[3])

def p_scope(p):
    """
    scope : LBRACE stmts RBRACE
    """
    p[0] = p[2]

def p_stmts_empty(p):
    """
    stmts :
    """
    p[0]=[]

def p_stmts_multi(p):
    """
    stmts : stmts stmt
    """
    p[0] = p[1] + [p[2]]

def p_stmts_single(p):
    """
    stmts : stmt
    """
    p[0] = [p[1]]

def p_stmt_expr(p):
    """
    stmt : expr
    """
    p[0] = p[1]

def p_params_empty(p):
    """
    params :
    """
    p[0] = []

def p_params_list(p):
    """
    params : param_list
    """
    p[0] = p[1]

def p_param_list_single(p):
    """
    param_list : param
    """
    p[0] = [p[1]]

def p_param_list_multi(p):
    """
    param_list : param_list COMMA param
    """
    p[0] = p[1] + [p[3]]

def p_param(p):
    """
    param : str COLON ID
          | num COLON ID
          | User COLON ID
    """
    p[0] = Ast('param', type=p[1], name=p[3])

def p_args_empty(p):
    """
    args :
    """
    p[0] = []

def p_args_list(p):
    """
    args : arg_list
    """
    p[0] = p[1]

def p_arg_list_single(p):
    """
    arg_list : expr
    """
    p[0] = [p[1]]

def p_arg_list_multi(p):
    """
    arg_list : arg_list COMMA expr
    """
    p[0] = p[1] + [p[3]]

def p_expr_binop(p):
    """
    expr : expr PLUS expr
         | expr MINUS expr
         | expr MULTIPLY expr
         | expr DIVIDE expr
         | expr MODULO expr
    """
    p[0] = Ast('binop', left=p[2], op=p[1], right=p[3])

def p_expr_value(p):
    """
    expr : ID
         | STR
         | NUM
         | FLT
    """
    p[0] = p[1]

# =====================
# ERROR
# =====================
def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at {p.value}")
    else:
        raise SyntaxError("Syntax error at EOF")

parser = yacc.yacc()
