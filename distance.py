import sympy as sp
import math
import argparse
import sys
from fractions import Fraction

import sympy.core.numbers


class Point():
    def __init__(self, numberOfCoordinates: int = None, listOfCoordinates: list = None, info: str = "Point: "):
        self.coordinates = []
        if numberOfCoordinates is None and listOfCoordinates is None:
            rawInput = input(info)
            coordinates = rawInput.split(',')
            self.dimensions = len(coordinates)
            for i in range(self.dimensions):
                self.coordinates.append(float(coordinates[i]))
        else:
            self.dimensions = numberOfCoordinates
            self.coordinates = listOfCoordinates

    def output(self):
        outputString = """P("""
        for coordinate in self.coordinates:
            outputString += str(beautify(coordinate)) + "|"
        outputString = outputString.rstrip("|") + ")"
        return outputString


class Line():
    def __init__(self, sv: list = None, dv: list = None, info = "Enter the coordinates of the vectors of the line separated by commas and then press the Enter key"):
        # If the user is to make the entries
        if sv is None or dv is None:
            print(info)

            def vectorInput():
                self.sv = input("support vector: ")
                if self.sv.endswith(','):
                    self.sv = self.sv[:-1]
                self.sv = self.sv.split(",")
                for i in range(len(self.sv)):
                    self.sv[i] = float(self.sv[i].strip())

                self.dv = input("direction vector: ")
                if self.dv.endswith(","):
                    self.dv = self.dv[:-1]
                self.dv = self.dv.split(",")
                for i in range(len(self.dv)):
                    self.dv[i] = float(self.dv[i].strip())

            vectorInput()
            while len(self.sv) != len(self.dv):
                print(
                    "The support vector does not have the same number of coordinates as the direction vector. Try again.")
                vectorInput()
        else:
            self.sv = sv
            self.dv = dv


class Plane():
    def __init__(self, normalVector: list = None, number=None, info: str = "In what form is the plane given?"):
        if normalVector is None and number is None:
            option = int(input(f"""{info}
1. parametric form
2. normal form
3. coordinate form\nChoose: """))
            # When a plane is entered in parametric form
            if option == 1:
                def vectorInput():
                    self.sv = input("support vector: ").split(',')
                    for i in range(len(self.sv)):
                        self.sv[i] = float(self.sv[i])
                    self.dv1 = input("1. direction vector: ").split(",")
                    for i in range(len(self.dv1)):
                        self.dv1[i] = float(self.dv1[i])
                    self.dv2 = input("2. direction vector: ").split(",")
                    for i in range(len(self.dv2)):
                        self.dv2[i] = float(self.dv2[i])

                vectorInput()
                while len(self.sv) != len(self.dv1) or len(self.sv) != len(self.dv2) or len(self.dv1) != len(self.dv2):
                    print("The vectors entered do not have the same number of coordinates. Try again.")
                    vectorInput()
                n1 = (self.dv1[1] * self.dv2[2]) - (self.dv1[2] * self.dv2[1])
                n2 = (self.dv1[2] * self.dv2[0]) - (self.dv1[0] * self.dv2[2])
                n3 = (self.dv1[0] * self.dv2[1]) - (self.dv1[1] * self.dv2[0])
                self.normalVector = [n1, n2, n3]
                self.number = float((n1 * self.sv[0]) + (n2 * self.sv[1]) + (n3 * self.sv[2]))

            # When a plane is entered in normal form
            if option == 2:
                def vectorInput():
                    self.normalVector = input("normal vector: ").split(',')
                    for i in range(len(self.normalVector)):
                        self.normalVector[i] = float(self.normalVector[i])

                vectorInput()
                print("Now enter a point in the plane")
                point = Point(info="Point in plane: ")
                value = 0
                for i in range(len(point.coordinates)):
                    value += self.normalVector[i] * point.coordinates[i]
                self.number = float(value)

            # When a plane is entered in coordinate form
            if option == 3:
                def vectorInput():
                    self.normalVector = input("normal vector: ").split(',')
                    for i in range(len(self.normalVector)):
                        self.normalVector[i] = float(self.normalVector[i])

                vectorInput()
                self.number = float(input("value on the other side of the '=' (constant term): "))

        else:
            self.normalVector = normalVector
            self.number = number


# Create parser and add arguments for points, lines and planes
class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    def format_help(self):
        custom_help = """You can calculate the distance between points, lines and planes.
        After the program you write for the calculations:
        -pt -pt => two points
        -pt -l => point & line
        -pt -pl => point & plane
        -l -l => two lines
        -l -pl => line & plane
        -pl -pl => two planes
        In what order you specify the components doesn't matter.
        For the input of coordinates, e.g. of a point, you enter them separated by commas. For comma numbers you use the one point instead of a comma."""
        return custom_help


parser = MyArgumentParser()
parser.add_argument('-pt', '--point', action='count', default=0, help='Adds a point to the calculation')
parser.add_argument('-l', '--line', action='count', default=0, help='Adds a layer to the calculation')
parser.add_argument('-pl', '--plane', action='count', default=0, help='Adds a plane to the calculation')



def checkWantedCalculation():
    args = parser.parse_args()
    return {
        "points": args.point,
        "lines": args.line,
        "planes": args.plane
    }


def connectionVector(p1: Point, p2: Point):
    new_vec = []
    for i in range(len(p1.coordinates)):
        new_vec.append(p1.coordinates[i] - p2.coordinates[i])
    return new_vec


def collinear(vector1, vector2):
    t = sp.symbols("t")
    eqs = []
    for i in range(len(vector1)):
        eqs.append(sp.Eq(vector1[i], vector2[i]*t))
    solved_eqs = []
    for eq in eqs:
        solved_eqs.append(sp.solve(eq))
    if all(x == solved_eqs[0] for x in solved_eqs):
        return True
    else:
        return False

def vectorLength(vector: list):
    sum = 0
    for coordinate in vector:
        sum += coordinate * coordinate
    return math.sqrt(sum)


# Transforms ugly floating point numbers into a more suitable format (round, convert to integer, to fraction or root) before outputting them to the console.
def beautify(number: float):
    def checkSquareRoot(n):
        square = round(n ** 2)
        root = math.sqrt(square)
        if abs(root - n) < 1e-10:  # You can adjust the accuracy here
            return f'{square}'
        else:
            return False

    def checkDecimalPlaces(number: float):
        number_str = str(number)
        if "." in number_str:
            return len(number_str.split(".")[1])
        else:
            return 0

    def checkRoundFraction(number:float):
        fraction = Fraction(number).limit_denominator()
        if len(str(fraction.numerator)) > 2 or len(str(fraction.denominator)) > 2:
            return False
        else:
            return len(str(fraction.numerator)), len(str(fraction.denominator))

    # For a smooth number, without decimal places
    if number.is_integer():
        return int(number)
    else:
        rounded = round(number, 4)
        # If it is a square root
        if checkSquareRoot(number):
            if rounded.is_integer():
                if rounded.is_integer() == int(1.0):
                    return str(1)
                else:
                    return f"{int(rounded)} or √{checkSquareRoot(number)}"
            else:
                return f"√{checkSquareRoot(number)} or approx. {rounded}"
        # In case of more than 4 decimal places and ugly fraction
        elif checkDecimalPlaces(number) > 4 and checkRoundFraction(number) is False:  # If it is not a smooth number, not a smooth root of, and not a smooth fraction
            return f"approx. {rounded}"
        # With more than four decimal places and "nice" fraction
        elif checkDecimalPlaces(number) > 4 and checkRoundFraction(number) is not False:
            return str(Fraction(number).limit_denominator())
        # For all other cases, i.e. more than four decimal places, ugly fraction and no "nice" root
        else:
            return f"approx. {rounded} or {Fraction(number).limit_denominator()}"


def generalConnectionVectorPointLine(point: Point, line: Line):
    new_vec = []
    t = sp.symbols('t')
    for i in range(len(point.coordinates)):
        new_vec.append(point.coordinates[i] - (line.sv[i] + (t * line.dv[i])))
    return new_vec


def generalConnectionVectorLineLine(line1, line2):
    new_vec = []
    r = sp.symbols('r')
    s = sp.symbols('s')
    for i in range(len(line1.sv)):
        new_vec.append((line1.sv[i] + r * line1.dv[i]) - (line2.sv[i] + s * line2.dv[i]))
    return new_vec



def auxiliaryLine(normalVector: list, point: Point):
    sv = []
    dv = []
    for i in range(len(normalVector)):
        sv.append(point.coordinates[i])
        dv.append(normalVector[i])
    return Line(sv, dv)


def parameterOrthogonalPunktLine(generalConnectionVector, Vector2) -> float:
    sum = 0
    for i in range(len(generalConnectionVector)):
        sum += generalConnectionVector[i] * Vector2[i]
    equation = sp.Eq(0, sum)
    solution = sp.solve(equation)[0]
    return float(sp.solve(equation)[0])


def pointOfLineAndParameters(line: Line, parameter: float) -> Point:
    t = sp.symbols('t')
    vec = []
    for i in range(len(line.sv)):
        vec.append(line.sv[i] + parameter * line.dv[i])
    return Point(len(vec), vec)


def dotProduct(vector1, vector2):
    sum = 0
    for i in range(len(vector1)):
        sum += vector1[i]*vector2[i]
    return sum


def plumbPointFromPlaneAndLine(plane: Plane, l: Line):
    t = sp.symbols('t')
    equation_string = 0
    for i in range(len(l.sv)):
        equation_string += (plane.normalVector[i] * (l.sv[i] + l.dv[i] * t))
    equation = sp.Eq(equation_string, plane.number)
    par = float(sp.solvers.solve(equation)[0])
    if isinstance(l.sv, tuple):
        l.sv = l.sv[0]
    return pointOfLineAndParameters(l, par)


def checkPositionRelationship(line1: Line, line2: Line):
    r = sp.symbols('r')
    s = sp.symbols('s')
    l1_equations = []
    l2_equations = []
    for i in range(len(line1.dv)):
        l1_equations.append(r*line1.dv[i])
        l2_equations.append(line2.dv[i])
    solved_equations = []
    for i in range(len(l1_equations)):
        equation = sp.Eq(l1_equations[i], l2_equations[i])
        solved_equations.append(sp.solvers.solve(equation))
    if all(x == solved_equations[0] for x in solved_equations):
        return "parallel or identical"
    else:
        solved_equations = []
        new_equations = []
        for equation in solved_equations:
            new_equations.append(sp.Eq(r, equation[r]))
        solutions = sp.solve(new_equations, [r, s])
        if len(solutions) == 0:
            return "skew"
        else:
            point = pointOfLineAndParameters(line1, float(solutions[r]))
            return f"intersecting {point.output()}"

if __name__ == "__main__":
    toCalc = checkWantedCalculation()
    if toCalc["points"] + toCalc["lines"] + toCalc["planes"] > 2:
        print("Only distances between points, planes and straight lines can be calculated. More than two specifications (e.g. two points) is not possible.")
        sys.exit()
    elif toCalc["points"] == 2:
        # Distance between two points
        p1 = Point(info="Enter the coordinates of the first point separated by commas, then press Enter.\n1. Point: ")
        p2 = Point(info="\nNow that of the second point: \n2. Point: ")
        v = connectionVector(p1, p2)
        d = beautify(vectorLength(v))
        print(f"\ndistance: {d} LU")
    elif toCalc["points"] == 1:
        p = Point(info="Enter the coordinates of the point separated by commas and then press Enter.\npoint: ")
        if toCalc["lines"] == 1:
            # distance zwischen Point und Line
            l = Line(info="\nNow enter the coordinates of the straight line")
            pg: list = generalConnectionVectorPointLine(p, l)  # Calculate the general connection vector from the entered point and the Line
            par = float(parameterOrthogonalPunktLine(pg, l.dv))  # Calculate the parameter for the Line, for the Point with the smallest distance
            point: Point = pointOfLineAndParameters(l, par)  # Calculate the point on the straight line closest to the point
            connectionVector = connectionVector(p, point)
            distance = vectorLength(connectionVector)
            print(f"\nparameter of the Line: {beautify(par)}")
            print(f"next Point on the Line: {point.output()}")
            print(f"distance: {beautify(distance)} LU")
        if toCalc["planes"] == 1:
            # Distance between point and plane
            e = Plane()
            auxiliaryLine = auxiliaryLine(e.normalVector, p)
            perpendicularFoot = plumbPointFromPlaneAndLine(e, auxiliaryLine)
            print(f"\nperpendicular foot: {perpendicularFoot.output()}")
            distance = vectorLength(connectionVector(p, perpendicularFoot))
            print(f"distance: {beautify(distance)} LU")

    elif toCalc["points"] == 0:
        if toCalc["lines"] == 2:
            # distance between two lines
            l1 = Line(info="Enter the coordinates of the first straight line separated by commas and then press the Enter key")
            l2 = Line(info="\nNow the second line: ")
            positionalReference = checkPositionRelationship(l1, l2)
            if positionalReference == "parallel or identical":
                p = Point(numberOfCoordinates=len(l1.sv), listOfCoordinates=l1.sv)  # support point der Line 1
                generalConnectionVector = generalConnectionVectorPointLine(p, l2)  # Allgemeiner Verbindungsvektor zwischen diesem Point und der Geraden 2
                par = parameterOrthogonalPunktLine(generalConnectionVector, l2.dv)  # Parameter für geringsten distance berechnen
                closest_point = pointOfLineAndParameters(l2, par)
                connectionVector = connectionVector(p, closest_point)
                distance = vectorLength(connectionVector)
                if distance == 0.0:
                    print(f"distance: 0, the lines are identical")
                else:
                    print(f"distance: {beautify(distance)}")
            elif "intersecting" in positionalReference:
                print(f"\ndistance: 0, the lines intersect in the point {positionalReference.replace('intersecting ', '')}")
            elif positionalReference == "skew":
                generalConnectionVector = generalConnectionVectorLineLine(l1, l2)
                eq1 = dotProduct(generalConnectionVector, l1.dv)
                r, s = sp.symbols('r s')
                eq2 = dotProduct(generalConnectionVector, l2.dv)
                solutions = sp.solve([eq1, eq2], [r, s])
                punkt_l1 = pointOfLineAndParameters(l1, float(solutions[r]))
                punkt_l2 = pointOfLineAndParameters(l2, float(solutions[s]))

                connectionVector = connectionVector(punkt_l2, punkt_l1)
                distance = vectorLength(connectionVector)

                if distance == 0.0:
                    print(f"\ndistance: 0, die Geraden schneiden sich in im Point {punkt_l1.output()}, da ihre support point identical sind.")
                else:
                    print(f"\nNächster Point auf 1. Line: {punkt_l1.output()}")
                    print(f"Nächster Point auf 2. Line: {punkt_l2.output()}")
                    print(f"distance: {beautify(distance)} LU")

        elif toCalc["lines"] == 1:
            if toCalc["planes"] == 1:
                # distance zwischen einer Geraden und einer Plane
                l = Line(info="Gib die Koordinaten der Geraden durch Kommas getrennt ein und drücke dann die Eingabetaste ")
                e = Plane(info="\nWähle jetzt die Form, in der die Plane gegeben ist: ")
                hilfspunkt = Point(numberOfCoordinates=len(l.sv), listOfCoordinates=l.sv)
                auxiliaryLine = auxiliaryLine(e.normalVector, hilfspunkt)
                perpendicularFoot = plumbPointFromPlaneAndLine(e, auxiliaryLine)
                print(f"\nperpendicular foot: {perpendicularFoot.output()}")
                distance = vectorLength(connectionVector(hilfspunkt, perpendicularFoot))
                print(f"distance: {beautify(distance)} LU")
        elif toCalc["planes"] == 2:
            # distance zwischen zwei Ebenen
            e1 = Plane(info="In welcher Form ist die erste Plane gegeben?")
            e2 = Plane(info="\nIn welcher Form ist die zweite Plane gegeben?")
            if collinear(e1.normalVector, e2.normalVector) == False:
                print("distance: 0, die Ebenen schneiden sich")
            else:
                x1 = sp.symbols('x1')
                equation = sp.Eq(e1.number, e1.normalVector[0]*x1)
                parameter_spurpunkt_x1 = float(sp.solve(equation)[0])
                x1_achse = Line(sv=[0.0, 0.0, 0.0], dv=[1.0, 0.0, 0.0])
                spurpunkt_x1 = pointOfLineAndParameters(x1_achse, parameter_spurpunkt_x1)

                auxiliaryLine = auxiliaryLine(e1.normalVector, spurpunkt_x1)
                lfp = plumbPointFromPlaneAndLine(e2, auxiliaryLine)
                distance = vectorLength(connectionVector(lfp, spurpunkt_x1))
                if distance == 0:
                    print(f"\ndistance: 0 LU, die Ebenen sind identical.")
                else:
                    print(f"\ndistance: {beautify(distance)} LU")
