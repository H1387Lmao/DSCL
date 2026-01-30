import ply.yacc as yacc
from .lexer import *
from .errors import *

def AstView(node, prefix="", is_last=True, ITEM_NAME=None):
    if not isinstance(node, Ast):
        return ""
    res = prefix
    name = ITEM_NAME+": " if ITEM_NAME is not None else ""
    if prefix:
        res += f"[dark gray]└── [?]" if is_last else f"[dark Gray]├── [?]"
    res += f"[gold]{name}Ast({node.n})[?]\n"

    child_prefix = prefix + ("    " if is_last else f"[dark Gray]│   [?]")

    items = [(k, v) for k, v in node.__dict__.items() if k != "n"]

    for i, (k, v) in enumerate(items):
        last = i == len(items) - 1

        if isinstance(v, Ast):
            res += AstView(v, child_prefix, last, ITEM_NAME=k)

        elif isinstance(v, list):
            res += child_prefix
            res += f"[dark Gray]└── [?]" if last else f"[dark Gray]├── [?]"
            res += f"[blue]{k} (List) \n[?]"

            for j, item in enumerate(v):
                res += AstView(
                    item,
                    child_prefix + ("    " if last else f"[dark Gray]│   [?]"),
                    j == len(v) - 1,
                )

        else:
            res += child_prefix
            res += f"[dark Gray]└── [?]" if last else f"[dark Gray]├── [?]"
            if isinstance(v, str):
                color = "[green]"
            elif isinstance(v, bool):
                color = "[red]"
            elif isinstance(v, int):
                color = "[purple]"
            else: color=""
            res += f"{k}: {color}{repr(v)}\n[?]"
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
    stmt : cmd ID LPAREN params RPAREN ARROW ID scope
    """
    p[0] = Ast('cmd_decl', is_async=True, name=p[2], args=p[4], stmts=p[8], target=p[7])

def p_func_decl(p):
    """
    fn_decl : fn ID LPAREN params RPAREN scope
    """
    p[0] = Ast('fn_decl', is_async=False, name=p[2], args=p[4], stmts=p[6])

def p_func(p):
    """
    stmt : async fn_decl
         | fn_decl
    """
    if len(p)==2:
        p[0]=p[1]
    else:
        p[2].is_async=True
        p[0]=p[2]

def p_lambda(p):
    """
    expr : fn LPAREN params RPAREN scope
         | async fn LPAREN params RPAREN scope
    """
    n=1 if p[1]=="async" else 0
    p[0] = Ast('lambda_decl', is_async=n==1, name=None, args=p[n+3], stmts=p[n+5])

def p_call(p):
    """
    expr : await expr LPAREN args RPAREN
         | expr LPAREN args RPAREN
    """
    n=1 if len(p)==6 else 0
    p[0] = Ast('call', name=p[n+1], args=p[n+3], awaited=n==1)

def p_construct(p):
    """
    expr : new expr LPAREN args RPAREN
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
    param : String COLON ID
          | Number COLON ID
          | User COLON ID
          | Context COLON ID
    """
    p[0] = Ast('param', type=p[1], name=p[3])

def p_args_empty(p):
    """
    arg_list :
    """
    p[0] = []

def p_args_list(p):
    """
    args : arg_list
    """
    p[0] = p[1]

def p_arg_list_single(p):
    """
    arg_list : arg_entry
    """
    p[0] = [p[1]]

def p_arg_list_multi(p):
    """
    arg_list : arg_list COMMA arg_entry
    """
    p[0] = p[1] + [p[3]]

def p_arg_entry(p):
    """
    arg_entry : expr
              | ID EQUALS expr
    """
    p[0]=p[1:]

def p_expr_binop(p):
    """
    expr : expr op expr

    """
    p[0] = Ast('binop', left=p[1], op=p[2], right=p[3])
def p_expr_operation(p):
    """
    op : PLUS
       | MINUS
       | MULTIPLY
       | DIVIDE
       | MODULO
    """
    p[0]=p[1]

def p_operation_reassign(p):
    """
    reop : op EQUALS
         | EQUALS
    """
    p[0]="".join(p[1:])
    
def p_expr_value(p):
    """
    expr : ID
         | STRING
         | NUM
         | FLT
         | getattr
    """
    p[0] = p[1]

def p_expr_string(p):
    """
    STRING : STR
    """
    p[0] = Ast("string", value=p[1])

def p_expr_group(p):
    """
    expr : LPAREN expr RPAREN
         | LBRACKET arg_list RBRACKET
    """
    p[0] = Ast("group", target=p[2])

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
    stmt : ID reop expr
    """
    p[0]=Ast(
        'var_resign', 
        name=p[1],
        operator=p[2],
        value=p[3]
    )

def p_getattr(p):
    """
    getattr : getattr ARROW expr
            | expr ARROW expr
            | expr DOT expr
            | getattr DOT expr
    """
    if isinstance(p[1], Ast) and p[1].n=="getattr":
        p[1]=[p[1].root, p[1].target]
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

def p_import(p):
    """
    stmt : use ID
    """
    p[0]=Ast(
        "import",
        target=p[2]
    )

def p_use_pkg(p):
    """
    stmt : use pkg DOUBLECOLON ID
    """
    p[0]=Ast(
        "usepkg",
        target=p[4]
    )

def p_if_stmt(p):
    """
    stmt : if cond scope elseifs else_stmt
    """
    p[0]=Ast(
        "if",
        cond=p[2],
        stmts=p[3],
        elseifs=p[4],
        else_stmt=p[5]
    )

def p_elseifs_single(p):
    """
    elseifs : elseif cond scope
    """
    p[0]=[Ast(
        "elseif",
        cond=p[2],
        stmts=p[3]
    )]
def p_elseifs_multiple(p):
    """
    elseifs : elseifs elseif cond scope
    """
    p[1]+=Ast(
        "elseif",
        cond=p[3],
        stmts=p[4]
    )
    p[0]=p[1]

def p_elseifs_none(p):
    """
    elseifs :
    """
    p[0]=[]

def p_else_none(p):
    """
    else_stmt :
    """

def p_else(p):
    """
    else_stmt : else scope
    """
    p[0]=Ast(
        "else",
        stmts=p[2]
    )

def p_cond_single(p):
    """
    cond : expr
    """
    p[0]=Ast(
        "cond",
        left=p[1],
        op=None,
        right=None
    )

def p_cond_compare(p):
    """
    cond : expr cmp expr
    """
    p[0]=Ast(
        "cond",
        left=p[1],
        op=p[2],
        right=p[3]
    )

def p_cmp(p):
    """
    cmp : EQS
        | NEQS
        | MEQS
        | LEQS
        | LT
        | MT
    """
    p[0]=p[1]

def p_while(p):
    """
    stmt : while cond scope
    """
    p[0]=Ast(
        "while",
        cond=p[2],
        stmts=p[3]
    )
def p_range_expr(p):
    """
    expr : expr to expr
    """
    p[0]=Ast(
        "range",
        min=p[1],
        max=p[3]
    )
def p_for(p):
    """
    stmt : for ID COLON expr scope
         | for ID in expr scope
         | for expr scope
    """
    target = p[2] if len(p)==6 else None
    cond = p[4] if target else p[2]
    stmts=p[5] if target else p[3]
    p[0]=Ast(
        "for",
        target=target,
        cond=cond,
        stmts=stmts
    )

def p_access(p):
    """
    expr : expr LBRACKET expr RBRACKET
    """
    p[0]=Ast(
        "access",
        parent=p[1],
        target=p[3]
    )

ParserLogger = Logger("Parser")

def p_error(p):
    if p:
        SyntaxError(ParserLogger, f"Unexpected token '{p.value}'", p.lineno, p.lexpos)
    else:
        SyntaxError(ParserLogger, f"Unexpected token at EOF")
    ParserLogger.exit_stage()
parser = yacc.yacc(debug=False)
