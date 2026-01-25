import ply.yacc as yacc
from .lexer import *

Ansi="\033["

Yellow=Ansi+"93m"
Green=Ansi+"92m"
Red=Ansi+"91m"
Blue=Ansi+"96m"
Purple=Ansi+"94m"
Reset=Ansi+"0m"
Gray=Ansi+"90m"

def AstView(node, prefix="", is_last=True):
    if not isinstance(node, Ast):
        return ""

    res = prefix
    if prefix:
        res += f"{Gray}└── {Reset}" if is_last else f"{Gray}├── {Reset}"
    res += f"{Blue}Ast({node.n}){Reset}\n"

    child_prefix = prefix + ("    " if is_last else f"{Gray}│   {Reset}")

    items = [(k, v) for k, v in node.__dict__.items() if k != "n"]

    for i, (k, v) in enumerate(items):
        last = i == len(items) - 1

        if isinstance(v, Ast):
            res += AstView(v, child_prefix, last)

        elif isinstance(v, list):
            res += child_prefix
            res += f"{Gray}└── {Reset}" if last else f"{Gray}├── {Reset}"
            res += f"{Purple}{k} (List) \n{Reset}"

            for j, item in enumerate(v):
                res += AstView(
                    item,
                    child_prefix + ("    " if last else f"{Gray}│   {Reset}"),
                    j == len(v) - 1
                )

        else:
            res += child_prefix
            res += f"{Gray}└── {Reset}" if last else f"{Gray}├── {Reset}"
            res += f"{k}: {repr(v)}\n{Reset}"
    return res

class Ast:
    def __init__(self, n, **args):
        self.n = n
        for k, v in args.items():
            setattr(self, k, v)
    def __repr__(self):
        return AstView(self)

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'MODULO')
)

def p_prog(p):
    """
    prog : stmts
    """
    p[0] = Ast('prog', stmts=p[1])

def p_cmd_def(p):
    """
    stmt : cmd ID LPAREN params RPAREN scope
    """
    p[0] = Ast('cmd_decl', name=p[2], args=p[4], stmts=p[6])

def p_call(p):
    """
    expr : expr LPAREN args RPAREN
    """
    p[0] = Ast('call', name=p[1], args=p[3])

def p_construct(p):
    """
    expr : new ID LPAREN args RPAREN
    """
    p[0] = Ast('construct', name=p[2], args=p[4])

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
    p[0] = Ast('binop', left=p[1], op=p[2], right=p[3])

def p_expr_value(p):
    """
    expr : ID
         | STR
         | NUM
         | FLT
         | getattr
    """
    p[0] = p[1]

def p_assign(p):
    """
    stmt : mut ID EQUALS expr
         | const ID EQUALS expr
    """
    p[0]=Ast(
        'var_decl', 
        type=p[1],
        name=p[2],
        value=p[4]
    )

def p_reassign(p):
    """
    stmt : ID EQUALS expr
    """
    p[0]=Ast(
        'var_resign', 
        name=p[1],
        value=p[3]
    )

def p_getattr(p):
    """
    getattr : getattr ARROW ID
            | ID ARROW ID
    """
    if isinstance(p[1], Ast):
        p[1]=[p[0].root, p[0].target]
    p[0]=Ast(
        "getattr",
        root=p[1],
        target=p[3]
    )
def p_setattr(p):
    """
    stmt : getattr EQUALS expr
    """
    p[0]=Ast(
        'var_resign', 
        name=p[1],
        value=p[3]
    )

def p_use(p):
    """
    stmt : use ID
    """
    p[0]=Ast(
        "import",
        target=p[2]
    )

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at {p.value} {p.lexer.lineno}")
    else:
        raise SyntaxError("Syntax error at EOF")

parser = yacc.yacc()
