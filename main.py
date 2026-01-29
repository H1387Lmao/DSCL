from src.lexer import *
from src.parser import *
from src.codegen import *

import sys
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument(nargs="?", dest="i")
argparser.add_argument("-o", "-output")
argparser.add_argument("-db", "-debug", dest='db', action="store_true")

args = argparser.parse_args()

if args.i is None:
    print(
        parser.parse(input(">> "))
    )
else:
    o = open(args.i)

    ast=parser.parse(
        o.read()
    )
    o.close()
    print(ast) if args.db else 0

if args.o:
    target = args.o
else:
    if args.i:
        target = ".".join(args.i.split(".")[:-1])+'.py'
    else:
        target = None

if ast:
    res = BaseGenerator(ast).compile()
    if args.db:
        print(res)

if target:
    o = open(target, "w")
o.write(res)
o.close()

print(f"[{Green}COMPILED{Reset}] Successfully wrote {len(res.split("\n"))} lines to {target}")
