from .parser import Ast, Red, Reset, Blue, Yellow, Green, Gray, Purple
import sys

class BaseGenerator:
    def __init__(self, ast):
        self.ast = ast

        self.scopes = [{}]
        self.lambdas=0

    def compile(self):
        self.code = ""

        self._add_line("from dscl.runtime import *")

        self.compile_statements(self.ast.stmts)

        return self.code

    def compile_statements(self, stmts):
        if stmts:
            for stmt in stmts:
                self.compile_statement(stmt)
        else:
            self._add_line("pass")

    def _add_line(self, line):
        self.code += self.i+line + '\n'

    def _add(self, text):
        self.code += text

    def compile_arg(self, arg):
        if len(arg)==1:
            return self.compile_expr(arg[0])
        else:
            return arg[0]+"="+self.compile_expr(arg[2])

    def sort_args(self, arguments):
        args = []
        kwargs = []

        for _arg in arguments:
            arg = self.compile_arg(_arg)
            if isinstance(arg, str) and "=" in arg:
                kwargs.append(
                    arg
                )
            else:
                args.append(
                    arg
                )
        return args + kwargs
    def compile_args(self, args):
        res=""
        args = self.sort_args(args)
        for arg in args:
            res+=str(arg)+", "
        return res.rstrip(", ")

    def compile_call(self, expr, is_line=False):
        name = self.compile_expr(expr.name)
        args = self.compile_args(expr.args)
        awaited = "await " if expr.awaited else ""
        res = awaited+name+f"({args})"
        if not is_line:
            return res
        else:
            self._add_line(res)

    def compile_expr(self, expr):
        if isinstance(expr, str):
            return expr.strip()
        if isinstance(expr, list):
            return self.compile_args(expr)
        if not isinstance(expr, Ast):
            return expr
        match expr.n:
            case "binop":
                left = self.compile_expr(expr.left)
                right = self.compile_expr(expr.right)
                op = expr.op
                return f'{left} {op} {right}'
            case "string":
                return '"'+expr.value+'"'
            case "construct":
                if expr.args:
                    res = f"{self.compile_expr(expr.name)}("
                    args = self.compile_args(expr.args)
                    res+=args+")"
                else:
                    res = f"{self.compile_expr(expr.name)}()"
                return res
            case "getattr":
                if not isinstance(expr.root, list):
                    expr.root = [expr.root]
                expr.root.append(expr.target)
                return '.'.join(expr.root)
            case "access":
                return f"{self.compile_expr(expr.parent)}[{self.compile_expr(expr.target)}]"
            case "call":
                return self.compile_call(expr)
            case "group":
                p = "Table" if isinstance(expr.target, list) else ""
                return f"{p}({self.compile_expr(expr.target)})"
            case "range":
                left = self.compile_expr(expr.min)
                right = self.compile_expr(expr.max)

                return f"range({left}, {right})"
            case "lambda_decl":
                self.lambdas += 1
                expr.name="lamdba_"+str(self.lambdas)
                self.compile_fn(expr)
                return expr.name
            case _:
                print("unknown\n", expr)
                return ""

    @property
    def i(self):
        return (len(self.scopes)-1)*"  "

    @property
    def i2(self):
        return len(self.scopes)*"  "

    def compile_param_type(self, type):
        match type:
            case "num":
                return ": int"
            case _:
                return ": "+type

    def compile_params(self, args, is_command=False):
        res = "" if not is_command else "this, "
        for arg in args:
            res += f"{arg.name}{self.compile_param_type(arg.type)}, "
        return res.removesuffix(", ")

    def compile_condition(self, cond):
        left = self.compile_expr(cond.left)
        if cond.op:
            right=self.compile_expr(cond.right)
            return f"{left} {cond.op} {right}"
        return left

    def compile_branch(self, stmt, type):
        cond = " "+self.compile_condition(stmt.cond) if type != "else" else ""
        self._add_line(f"{type}{cond}:")
        self.scopes.append({})
        scope = self.compile_statements(stmt.stmts)
        self.scopes.pop()

    def search_var(self, n):
        for i in range(len(self.scopes)-1, -1, -1):
            if n in self.scopes[i]:
                return self.scopes[i][n]
    def compile_fn(self, stmt, is_cmd=False):
        if not is_cmd:
            _async = "async " if stmt.is_async else ""
        else:
            _async = "async "

        self._add_line(f"{_async}def {stmt.name}({self.compile_params(stmt.args, is_cmd)}):")
        self.scopes[-1][stmt.name]=("func", stmt.is_async)
        self.scopes.append({})

        self.compile_statements(stmt.stmts)
    
        self.scopes.pop()

    def decl_var(self, stmt):
        value = self.compile_expr(stmt.value)
        name = self.compile_expr(stmt.name)
        self._add_line(f"{name} = {value}")
                
        self.scopes[-1][name] = (stmt.type, value)


    def compile_statement(self, stmt):
        match stmt.n:
            case "import":
                self._add_line(f"import {stmt.target}")
            case "var_decl":
                self.decl_var(stmt)
            case "cmd_decl":
                self._add_line(f"@{stmt.target}.slash_command")
                self.compile_fn(stmt, True)
            case "fn_decl":
                self.compile_fn(stmt)
            case "var_resign":
                name = self.compile_expr(stmt.name)
                value = self.compile_expr(stmt.value)
                op=stmt.operator if hasattr(stmt, "operator") else "="
                if '.' not in name:
                    v = self.search_var(name)
                    if v is None:
                        stmt.type="mut"
                        self.decl_var(stmt)
                        return
                    elif v[0] == "const":
                        raise Exception("Tried to edit a constant variable!")
                self._add_line(f"{name} {op} {value}")
            case "usepkg":
                match stmt.target:
                    case "discord":
                        self._add_line("from dscl.discord import *")
                    case "discordui":
                        self._add_line("from dscl.discord.ui import *")
                    case _:
                        print(f"{Red}[COMPILER]{Reset}Unknown package: '{stmt.target}'")
                        return
            case "call":
                self.compile_call(stmt, True)
            case "if":
                self.compile_branch(stmt, "if")
                for elseif in stmt.elseifs:
                    self.compile_branch(elseif, "elif")
                if stmt.else_stmt:
                    self.compile_branch(stmt.else_stmt, "else")
            case "while":
                cond = self.compile_condition(stmt.cond)
                self._add_line(f"while {cond}:")
                self.scopes.append({})
                self.compile_statements(stmt.stmts)
                self.scopes.pop()
            case "for":
                cond = self.compile_expr(stmt.cond)
                target = stmt.target if stmt.target else "_"
                self._add_line(f"for {target} in {cond}:")
                self.scopes.append({})
                self.compile_statements(stmt.stmts)
                self.scopes.pop()
            case _:
                self._add_line(self.compile_expr(stmt))
