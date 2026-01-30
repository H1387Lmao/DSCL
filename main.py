from src.lexer import *
from src.parser import *
from src.codegen import *
import sys
import argparse
import pathlib

def compile_dscl(args):
    if args.i is None:
        ast = parser.parse(input(">> "))
    else:
        with open(force_extension(args.i,"dscl"), "r", encoding="utf-8") as f:
            ast = parser.parse(f.read())
    if args.db:
        print(ast)
    if not ast:
        return
    res = BaseGenerator(ast).compile()
    if args.db:
        print(res)
    if args.o:
        target = force_extension(args.o,"py")
    else:
        if args.i:
            target = force_extension(args.i, "py")
        else:
            target = None
    if target:
        with open(target, "w", encoding="utf-8") as f:
            f.write(res)
        print(f"[{Green}COMPILED{Reset}] Successfully wrote {len(res.splitlines())} lines to {target}")
    return res
def run_python(file_path: str):
    file = pathlib.Path(force_extension(file_path, "py")).resolve()
    if not file.exists():
        print(f"{Red}Error: file not found: {file}")
        sys.exit(1)
    root = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(file.parent))
    globals_dict = {"__file__": str(file), "__name__": "__main__"}
    with open(file, "r", encoding="utf-8") as f:
        src = f.read()
    exec(compile(source=src, filename=str(file), mode="exec"), globals_dict)

def compile_target(i, target):
    with open(args.i, "r", encoding="utf-8") as f:
        ast = parser.parse(f.read())
    
    with open(target, "w") as f:
        f.write(BaseGenerator(ast).compile())
    return AstView(ast, no_color=True)

def force_extension(file, ext):
    return ".".join(file.split(".")[:-1])+"."+ext

def main():
    parser = argparse.ArgumentParser(prog="dscl")
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compile")
    c.add_argument("-o", "--output", dest="o")
    c.add_argument("i", nargs="?")
    c.add_argument("-db", "--debug", dest="db", action="store_true")
    c.add_argument("-no-color", "--nc", dest="nc", action="store_true")

    cr = sub.add_parser("compile_run")
    cr.add_argument("-no-color", "--nc", dest="nc", action="store_true")
    cr.add_argument("-o", "--output", dest="o")
    cr.add_argument("i", nargs="?")
    cr.add_argument("-db", "--debug", dest="db", action="store_true")

    r = sub.add_parser("run")
    r.add_argument("-db", "--debug", dest="db", action="store_true")
    r.add_argument("i", nargs="?")
    r.add_argument("-no-color", "--nc", dest="nc", action="store_true")

    args = parser.parse_args()
    SET_COLOR(bool(args.nc))
    if args.cmd == "compile":
        compile_dscl(args)
    if args.cmd == "run":
        run_python(force_extension(args.i, "py"))
    if args.cmd == "compile_run":
        compile_dscl(args)
        run_python(force_extension(args.i, "py"))

if __name__=="__main__":
    main()
