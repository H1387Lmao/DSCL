# DSCL (Programming Language)
[![DSCL - Website](https://img.shields.io/badge/DSCL-Website-blueviolet)](https://h1387lmao.github.io/DSCL)
[![dependency - ply](https://img.shields.io/badge/dependency-ply-blue?logo=python&logoColor=white)](https://pypi.org/project/ply)
![License](https://img.shields.io/badge/License-MIT-green)


[DSCL](https://h1387lmao.github.io/DSCL) is a programming language for making discord bots

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

To use a custom file target, run with a `-o` option

```sh
python main.py examples/hello.dscl -o examples/hello.py
```

> Pycord is the default dependency for now for easy use.
> Right until custom Discord Library is complete

After more library options are added
You can select them in the future by using the `-compiler=` flag

```sh
python main.py examples/hello.dscl -compiler=Pycord
```

## W.I.P Features

|  Features to add          |  Completed |
|:-------------------------:|:----------:|
|Transpiler for Pycord      |Yes         |
|Components V2 Integration  |No          |
|Custom Pycord Wrapper      |W.I.P       |
