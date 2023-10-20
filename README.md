# Geometry Distance Calculator

Welcome to the Geometry Distance Calculator! This program is designed to calculate distances between points, lines, and planes in three-dimensional space.

## Features
- **Point Distance Calculation**: Calculate the distance between two points in 3D space.
- **Line Distance Calculation**: Calculate the shortest distance between two lines in 3D space.
- **Plane Distance Calculation**: Calculate the distance from a point to a plane in 3D space.

Please note that while this program can handle points, lines, and planes, it is optimized for three-dimensional objects. The accuracy of calculations involving lines and planes may decrease in dimensions other than three.

## Usage
To specify what you want to calculate, use the following arguments:
- `-pt` for points
- `-l` for lines
- `-pl` for planes

These arguments do not require a value following them. They simply indicate to the program what type of calculation you wish to perform.

## Dependencies
This program requires the following Python libraries:
- `sympy`: A Python library for symbolic mathematics.
- `math`: A built-in Python library for mathematical tasks.
- `argparse`: A built-in Python library for writing user-friendly command-line interfaces.
- `sys`: A built-in Python library that provides access to some variables used or maintained by the Python interpreter.
- `fractions`: A built-in Python library for rational number arithmetic.

You can install any missing dependencies using pip:
`pip install sympy`
