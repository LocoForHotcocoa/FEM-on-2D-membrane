# my final project from Computational Physics (PHYS 163) at CSUS

This app computes the modes of the 2D wave equation on a circle with FEM and can be used for any continuous function for `f(R) = 0`.

It works for any user defined function!

## Installation
- *python 3.13 is required.*
1. clone repo:
```shell
git clone git@github.com:LocoForHotcocoa/FEM-on-2D-membrane.git
```
2. install package with pip or poetry
```shell

cd FEM-on-2D-membrane

# 1. with pip (recommended to use a venv to not mess up your local python env)
python3 -m venv .venv
source .venv/bin/activate
pip install .

# 2. or with poetry (venv is handled automatically)
poetry install
```

## How to Run
```shell
# get help menus:
fem --help
fem circle --help

# example function call:
fem circle 'cos(3*arctan2(y,x))*sin(pi*sqrt(x**2+y**2))' --num-elements 500 --speed 4
```

*TODO*: 
1. allow user to run the old version with no FEM (my actual submitted project from PHYS 163): 
2. allow user to run `line` to animate FEM on line


## Things that I'm currently working on:
- Make the tool more user-friendly
    - Somehow allow entire function to be read in by the user
    - Maybe json file for parameters? idk


