from src.lexer import *
from src.parser import *

import sys
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument(nargs="?", dest="i")
argparser.add_argument("-o", "-output")

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
    print(ast)
