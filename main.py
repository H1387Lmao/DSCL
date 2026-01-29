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
        with open(args.i, "r", encoding="utf-8") as f:
            ast = parser.parse(f.read())
    if args.db:
        print(ast)
    if not ast:
        return
    res = BaseGenerator(ast).compile()
    if args.db:
        print(res)
    if args.o:
        target = args.o
    else:
        if args.i:
            target = ".".join(args.i.split(".")[:-1]) + ".py"
        else:
            target = None
    if target:
        with open(target, "w", encoding="utf-8") as f:
            f.write(res)
        print(f"[{Green}COMPILED{Reset}] Successfully wrote {len(res.splitlines())} lines to {target}")
    return res
def process_code(source):
    ast = parser.parse(source)
    return (ast, BaseGenerator(ast).compile())
def run_python(file_path: str):
    file = pathlib.Path(file_path).resolve()
    if not file.exists():
        print(f"{Red}Error: file not found: {file}")
        sys.exit(1)
    root = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(file.parent))
    globals_dict = {"__file__": str(file), "__name__": "__main__"}
    with open(file, "r", encoding="utf-8") as f:
        src = f.read()
    exec(compile(src, str(file), "exec"), globals_dict)

def main():
    parser = argparse.ArgumentParser(prog="dscl")
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compile")
    c.add_argument("i", nargs="?")
    c.add_argument("-o", "--output", dest="o")
    c.add_argument("-db", "--debug", dest="db", action="store_true")
    r = sub.add_parser("run")
    r.add_argument("file")
    args = parser.parse_args()
    if args.cmd == "compile":
        return compile_dscl(args)
    elif args.cmd == "run":
        return run_python(args.file)
if __name__=="__main__":
    main()
