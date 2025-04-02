# my final project from Computational Physics (PHYS 163) at CSUS

This app computes the modes of the 2D wave equation on a circle with FEM and can be used for any continuous function for `f(R) = 0`.

It works for any user defined function!

## Installation
- *python 3.13 is required.*
- *if you want to save animations with `--show` flag, the software **`ffmpeg`** is required and must be in system path.*
    - if on mac, just download with homebrew: `brew install ffmpeg`
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
This supports animation on a 1D line: `fem line`, and a 2D circular membrane: `fem circle`

```shell
# get help menus:
fem --help
fem circle --help

# example function call:
fem circle 'cos(3*arctan2(y,x))*sin(pi*sqrt(x**2+y**2))' --num-elements 500 --speed 4
```

*TODO*: 
1. fix framerate: `--show`/`--save` are not the same framerate
2. idk what else to do


