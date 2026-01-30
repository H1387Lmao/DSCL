from src.lexer import *
from src.parser import *
from src.codegen import *
from src.hlog import Logger
import sys
import argparse
import pathlib
import os

MainLogger = Logger("MainLogger")

if os.name=="posix":
    import readline

def multi_input():
    print("Write 2 empty lines to finish")
    res = ""
    first = input(">>> ")+"\n"
    res+=first
    while True:
        first = input("... ").strip()
        if not first: break
        res+=first+"\n"
    return res

def set_files(inp):
    LexerLogger.file=inp
    ParserLogger.file=inp


def compile_dscl(args):
    if args.i is None:
        inp = multi_input()
        set_files(inp)
        ast = parser.parse(inp)
    else:
        i = force_extension(args.i, "dscl")
        if pathlib.Path(i).exists():
            with open(i, "r", encoding="utf-8") as f:
                r=f.read()
                set_files(r)
                ast = parser.parse(r)
            
        else:
            MainLogger.print(f"[[red]COMPILER[?]] File '{i}' was not found.")
            sys.exit(-1)
    if args.db:
        MainLogger.print(repr(ast))
    if not ast:
        return
    res = BaseGenerator(ast).compile()
    if args.db:
        MainLogger.print_code(res)
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
        MainLogger.print(f"[[green]COMPILED[?]] Successfully wrote {len(res.splitlines())} lines to {target}")
    ParserLogger.exit_stage()
    return res
def run_python(file_path: str):
    if "dscl.runtime" not in file_path:
        file = pathlib.Path(force_extension(file_path, "py")).resolve()
        if not file.exists():
            MainLogger.error(f"file not found: {file}")
            sys.exit(1)

        with open(file, "r", encoding="utf-8") as f:
            src = f.read()

        root = pathlib.Path(__file__).resolve().parent
        sys.path.insert(0, str(file.parent))
        sys.path.insert(0, str(root))

    else:
        file = "DSCL REPL"
        src = file_path

    globals_dict = {"__file__": str(file), "__name__": "__main__"}
    
    exec(compile(source=src, filename=str(file), mode="exec"), globals_dict)

def compile_target(i, target):
    LexerLogger.no_color=True
    ParserLogger.no_color=True
    with open(args.i, "r", encoding="utf-8") as f:
        r = f.read()
        set_files(r)
        ast = parser.parse(r)
    with open(target, "w") as f:
        f.write(BaseGenerator(ast).compile())
    return MainLogger.colorize(repr(ast))

def force_extension(file, ext):
    return ".".join(file.split(".")[:-1])+"."+ext

def main():
    parser = argparse.ArgumentParser(prog="dscl")
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compile")
    c.add_argument("-o", "--output", dest="o")
    c.add_argument("i", nargs="?")
    c.add_argument("-db", "--debug", dest="db", action="store_true")
    c.add_argument("--no-color", "-nc", dest="nc", action="store_true")

    cr = sub.add_parser("compile_run")
    cr.add_argument("--no-color", "-nc", dest="nc", action="store_true")
    cr.add_argument("-o", "--output", dest="o")
    cr.add_argument("i", nargs="?")
    cr.add_argument("-db", "--debug", dest="db", action="store_true")

    r = sub.add_parser("run")
    r.add_argument("-db", "--debug", dest="db", action="store_true")
    r.add_argument("i", nargs="?")
    r.add_argument("--no-color", "-nc", dest="nc", action="store_true")

    args = parser.parse_args()
    ParserLogger.no_colors=bool(args.nc)
    LexerLogger.no_colors=bool(args.nc)
    MainLogger.no_colors=bool(args.nc)

    if args.cmd == "compile":
        compile_dscl(args)
    if args.cmd == "run":
        run_python(force_extension(args.i, "py"))
    if args.cmd == "compile_run":
        res = compile_dscl(args)
        if args.i:
            run_python(force_extension(args.i, "py"))
        else:
            run_python(res)

if __name__=="__main__":
    main()
