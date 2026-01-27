from .parser import Ast, Red, Reset, Blue, Yellow, Green, Gray, Purple

class BaseGenerator:
	def __init__(self, ast):
		self.ast = ast

		self.scopes = [{}]

	def compile(self):
		self.code = ""

		self.compile_statements(self.ast.stmts)

		return self.code

	def compile_statements(self, stmts):
		for stmt in stmts:
			self.compile_statement(stmt)

	def _add_line(self, line):
		self.code += self.i+line + '\n'

	def _add(self, text):
		self.code += text

	def compile_call(self, expr, is_line=False):
		name = self.compile_expr(expr.name)
		res = f"{name}({", ".join(map(self.compile_expr, expr.args))})"
		if not is_line:
			return res
		else:
			self._add_line(res)

	def compile_expr(self, expr):
		if isinstance(expr, str):
			return expr.strip()
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
					res = f"{expr.name}(\n{self.i}  {f", \n{self.i}  ".join(map(self.compile_expr, expr.args))}\n{self.i})"
				else:
					res = f"{expr.name}()"
				return res
			case "getattr":
				if not isinstance(expr.root, list):
					expr.root = [expr.root]
				expr.root.append(expr.target)
				return '.'.join(expr.root)
			case "call":
				return self.compile_call(expr)
			case _:
				print("unknown\n", expr)
				return ""

	@property
	def i(self):
		return (len(self.scopes)-1)*"  "

	def compile_param_type(self, type):
		match type:
			case "User":
				return ": discord.Member"
			case "str":
				return ": str"
			case "num":
				return ": int"
			case _:
				return ""

	def compile_params(self, args, is_command=False):
		res = "" if not is_command else "this, "
		for arg in args:
			res += f"{arg.name}{self.compile_param_type(arg.type)}, "
		return res.removesuffix(", ")

	def compile_statement(self, stmt):
		print(stmt)
		match stmt.n:
			case "import":
				self._add_line(f"import {stmt.target}")
			case "var_decl":
				value = self.compile_expr(stmt.value)
				name = self.compile_expr(stmt.name)
				self._add_line(f"{name} = {value}")
				if stmt.type == "const":
					self.scopes[-1][name] = (stmt.type, value)
			case "cmd_decl":
				self._add_line(f"@{stmt.target}.slash_command")
				self._add_line(f"async def {stmt.name}({self.compile_params(stmt.args, True)}):")
				self.scopes.append({})

				self.compile_statements(stmt.stmts)
				
				self.scopes.pop()
			case "var_resign":
				name = self.compile_expr(stmt.name)
				value = self.compile_expr(stmt.value)
				if '.' not in name:
					if name not in self.scopes[-1]:
						print(f"{Red}[COMPILER]{Reset} Can't reassign variable that hasnt been declared yet!")
						return
					elif self.scopes[-1][name][0] == "const":
						print(f"{Red}[COMPILER]{Reset} Can't reassign variable that is a constant!")
						return
				self._add_line(f"{name}={value}")
			case "usepkg":
				match stmt.target:
					case "discord":
						self._add_line("from discord.ext import commands")
						self._add_line("from discord import Intents")
					case _:
						print(f"{Red}[COMPILER]{Reset}Unknown package: '{stmt.target}'")
						return
			case "call":
				self.compile_call(stmt, True)
			case _:
				self.compile_expr(stmt)
