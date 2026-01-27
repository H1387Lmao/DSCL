# DSCL (Programming Language)

DSCL is a programming language for making discord bots

## Installation

```sh
git clone https://github.com/H1387Lmao/DSCL.git
cd DSCL
pip install -r requirements
```

## Examples

There are some examples found in the examples folder,
including a result built by codegen.py

## Different modes

To use the compiler mode, run with a `-o` option

```sh
python main.py examples/hello.dscl -o bin/hello.py
```

> [!NOTE]
> Interpreter mode is not yet implemented
> it will default to the compiler option!
> please keep mind of this

To use the interpreter mode, run without any other options

```sh
python main.py examples/hello.dscl
```

## W.I.P Features

|  Features to add          |  Completed |
|:-------------------------:|:----------:|
|Transpiler for Pycord      |Yes         |
|Components V2 Integration  |No          |
|Interpreter Runtime        |No          |
|Better syntax (hopefully)  |Probably?   |
