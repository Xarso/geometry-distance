# Geometry Distance Calculator

Welcome to the Geometry Distance Calculator. This program is designed to calculate distances between points, lines, and planes in three-dimensional space using vectors.

## Features
- **Point Distance**: Calculate the distance between two points.
- **Point - Line Distance**: Calculate the shortest distance and get the closest point on the line.
- **Line Distance**: Calculate the shortest distance between two lines and get the points being closest to each other.
- **Plane - point - distance**: Calculate the shortest distance between a plane and a point and get the point on the plane being the closest to the other Point.
- **Plane - line - distance**: Calculate the shortest distance (if the plane and the line are parallel) or otherwise the point of intersection.
- **Plane - plane - distance**: Calculate the shortest distance between two planes.

Please note that while this program can handle points, lines, and planes, it is optimized for three-dimensional objects. The accuracy of calculations involving lines and planes will decrease in dimensions other than three.

## Usage
To specify what you want to calculate, use two of the following arguments:
- `-pt` for points
- `-l` for lines
- `-pl` for planes

These arguments do not require a value following them. They simply indicate to the program what type of calculation you wish to perform.

## Dependencies
This program requires the following external Python library:
- `sympy`: A Python library for symbolic mathematics.

You can install any missing dependencies using pip
