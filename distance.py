import sympy as sp
import math
import argparse
import sys
from fractions import Fraction

import sympy.core.numbers


class Point():
    def __init__(self, number_of_coordinates: int = None, liste_der_Koordinaten: list = None, info: str = "Point: "):
        self.coordinates = []
        if number_of_coordinates is None and liste_der_Koordinaten is None:
            eingabe = input(info)
            koordinaten = eingabe.split(',')
            self.dimensions = len(koordinaten)
            for i in range(self.dimensions):
                self.coordinates.append(float(koordinaten[i]))
        else:
            self.dimensions = number_of_coordinates
            self.coordinates = liste_der_Koordinaten

    def output(self):
        outputString = """P("""
        for coordinate in self.coordinates:
            outputString += str(beautify(coordinate)) + "|"
        outputString = outputString.rstrip("|") + ")"
        return outputString


class Gerade():
    def __init__(self, sv: list = None, rv: list = None, info = "Gib die Koordinaten der Vektoren der Gerade durch Kommas getrennt ein und drücke dann die Enter-Taste"):
        # Wenn der Nutzer die Eingaben machen soll
        if sv is None or rv is None:
            print(info)

            def vectorInput():
                self.sv = input("Stützvektor: ")
                if self.sv.endswith(','):
                    self.sv = self.sv[:-1]
                self.sv = self.sv.split(",")
                for i in range(len(self.sv)):
                    self.sv[i] = float(self.sv[i].strip())

                self.rv = input("Richtungsvektor: ")
                if self.rv.endswith(","):
                    self.rv = self.rv[:-1]
                self.rv = self.rv.split(",")
                for i in range(len(self.rv)):
                    self.rv[i] = float(self.rv[i].strip())

            vectorInput()
            while len(self.sv) != len(self.rv):
                print(
                    "Der Stützvektor hat nicht die gleiche Anzahl an Koordinaten wie der Richtungsvektor. Versuch's nochmal")
                vectorInput()
        else:
            self.sv = sv
            self.rv = rv


class Layer():
    def __init__(self, normalenvektor: list = None, number=None, info: str = "In welcher Form ist die Layer gegeben?"):
        if normalenvektor is None and number is None:
            option = int(input(f"""{info}
1. Parameterform (1)
2. Normalenform (2)
3. Koordinatenform (3)\nWähle: """))
            # Wenn die Layer in Parameterform eingegeben wird
            if option == 1:
                def vectorInput():
                    self.sv = input("Stützvektor: ").split(',')
                    for i in range(len(self.sv)):
                        self.sv[i] = float(self.sv[i])
                    self.rv1 = input("1. Richtungsvektor: ").split(",")
                    for i in range(len(self.rv1)):
                        self.rv1[i] = float(self.rv1[i])
                    self.rv2 = input("2. Richtungsvektor: ").split(",")
                    for i in range(len(self.rv2)):
                        self.rv2[i] = float(self.rv2[i])

                vectorInput()
                while len(self.sv) != len(self.rv1) or len(self.sv) != len(self.rv2) or len(self.rv1) != len(self.rv2):
                    print("Die eingegebenen Vektoren haben nicht die gleiche Anzahl an Koordinaten. Versuch's nochmal.")
                    vectorInput()
                n1 = (self.rv1[1] * self.rv2[2]) - (self.rv1[2] * self.rv2[1])
                n2 = (self.rv1[2] * self.rv2[0]) - (self.rv1[0] * self.rv2[2])
                n3 = (self.rv1[0] * self.rv2[1]) - (self.rv1[1] * self.rv2[0])
                self.normalenvektor = [n1, n2, n3]
                self.number = float((n1 * self.sv[0]) + (n2 * self.sv[1]) + (n3 * self.sv[2]))

            # Wenn eine Normalenform eingegeben wird:
            if option == 2:
                def vectorInput():
                    self.normalenvektor = input("Normalenvektor: ").split(',')
                    for i in range(len(self.normalenvektor)):
                        self.normalenvektor[i] = float(self.normalenvektor[i])

                vectorInput()
                print("Gibt jetzt einen Point in der Layer ein")
                point = Point(info="Point in Layer: ")
                value = 0
                for i in range(len(point.coordinates)):
                    value += self.normalenvektor[i] * point.coordinates[i]
                self.number = float(value)

            # Wenn eine Layer in Koordinatenform eingegeben wird
            if option == 3:
                def vectorInput():
                    self.normalenvektor = input("Normalenvektor: ").split(',')
                    for i in range(len(self.normalenvektor)):
                        self.normalenvektor[i] = float(self.normalenvektor[i])

                vectorInput()
                self.number = float(input("Wert auf der anderen Seite des '=': "))

        else:
            self.normalenvektor = normalenvektor
            self.number = number


# Parser erstellen und Argumente für Punkte, Geraden und Ebenen hinzufügen
class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('Fehler: %s\n' % message)
        self.print_help()
        sys.exit(2)

    def format_help(self):
        custom_help = """Du kannst den Abstand zwischen zwei Punkten, zwei Geraden, zwei Ebenen oder zwei dieser Elemente untereinander ausrechnen.
        Hinter das Programm schreibst du für die Berechnungen:
        -p -p => zwei Punkte
        -p -g => ein Punkte & eine Gerade
        -p -e => ein Punkte & eine Layer
        -g -g => zwei Geraden
        -g -e => eine Gerade & eine Layer
        -e -e => zwei Ebenen
        In welcher Reihenfolge du die Komponenten angibst, ist egal.
        Für die Eingabe von Koordinaten, z.B. von einem Point, gibst du sie durch Kommas getrennt ein. Bei Kommazahlen verwendest du den einen Point statt einem Komma"""
        return custom_help


parser = MyArgumentParser()
parser.add_argument('-p', '--punkt', action='count', default=0, help='Fügt einen Point zur Berechnung hinzu')
parser.add_argument('-g', '--gerade', action='count', default=0, help='Fügt eine Gerade zur Berechnung hinzu')
parser.add_argument('-e', '--ebene', action='count', default=0, help='Fügt eine Layer zur Berechnung hinzu')
parser.add_argument('--mein_arg', help='Zeigt Hilfe für das Programm an')


def checkWantedCalculation():
    args = parser.parse_args()
    return {
        "punkte": args.punkt,
        "geraden": args.gerade,
        "ebenen": args.ebene
    }


def verbindungsvektor(p1: Point, p2: Point):
    new_vec = []
    for i in range(len(p1.coordinates)):
        new_vec.append(p1.coordinates[i] - p2.coordinates[i])
    return new_vec


def kollinear(vektor1, vektor2):
    t = sp.symbols("t")
    eqs = []
    for i in range(len(vektor1)):
        eqs.append(sp.Eq(vektor1[i], vektor2[i]*t))
    solved_eqs = []
    for eq in eqs:
        solved_eqs.append(sp.solve(eq))
    if all(x == solved_eqs[0] for x in solved_eqs):
        return True
    else:
        return False

def vektorLänge(vektor: list):
    sum = 0
    for koordinate in vektor:
        sum += koordinate * koordinate
    return math.sqrt(sum)


# Verwandelt hässliche Fließkommazahlen vor der Ausgabe auf der Konsole in ein passenderes Format (runden, in Integer umwandeln, in Bruch oder Wurzel)
def beautify(number: float):
    def check_square_root(n):
        square = round(n ** 2)
        root = math.sqrt(square)
        if abs(root - n) < 1e-10:  # Sie können die Genauigkeit hier anpassen
            return f'{square}'
        else:
            return False

    def check_nachkommastellen(number: float):
        number_str = str(number)
        if "." in number_str:
            return len(number_str.split(".")[1])
        else:
            return 0

    def check_glatterBruch(number:float):
        bruch = Fraction(number).limit_denominator()
        if len(str(bruch.numerator)) > 2 or len(str(bruch.denominator)) > 2:
            return False
        else:
            return len(str(bruch.numerator)), len(str(bruch.denominator))

    # Bei einer glatten Zahl, ohne Nachkommastellen
    if number.is_integer():
        return int(number)
    # Sonst
    else:
        rounded = round(number, 4)
        # Wenn es eine Quadratwurzel ist
        if check_square_root(number):
            if rounded.is_integer():
                if rounded.is_integer() == int(1.0):
                    return str(1)
                else:
                    return f"{int(rounded)} oder √{check_square_root(number)}"
            else:
                return f"√{check_square_root(number)} oder ca. {rounded}"
        # Bei mehr als 4 Nachkommastellen und hässlichem Bruch
        elif check_nachkommastellen(number) > 4 and check_glatterBruch(number) is False:  # Wenn es keine glatte Zahl, keine glatte Wurzel aus und kein glatter Bruch ist
            return f"ca. {rounded}"
        # Bei mehr als vie Nachkommastellen und "schönem" Bruch
        elif check_nachkommastellen(number) > 4 and check_glatterBruch(number) is not False:
            return str(Fraction(number).limit_denominator())
        # Bei allen anderen Fällen, also mehr als vier Nachkommastellen, hässlichem Bruch und keiner "schönen" Wurzel
        else:
            return f"ca. {rounded} oder {Fraction(number).limit_denominator()}"


def allg_verb_vek_p_g(punkt: Point, gerade: Gerade):
    new_vec = []
    t = sp.symbols('t')
    for i in range(len(punkt.coordinates)):
        new_vec.append(punkt.coordinates[i] - (gerade.sv[i] + (t * gerade.rv[i])))
    return new_vec


def allg_verb_vek_g_g(gerade1, gerade2):
    new_vec = []
    r = sp.symbols('r')
    s = sp.symbols('s')
    for i in range(len(gerade1.sv)):
        new_vec.append((gerade1.sv[i] + r * gerade1.rv[i]) - (gerade2.sv[i] + s * gerade2.rv[i]))
    return new_vec



def hilfsgerade(normalenvektor: list, punkt: Point):
    sv = []
    rv = []
    for i in range(len(normalenvektor)):
        sv.append(punkt.coordinates[i])
        rv.append(normalenvektor[i])
    return Gerade(sv, rv)


def parameter_orthogonal_punkt_gerade(allgemeinerVerbindungsvektor, Vektor2) -> float:
    sum = 0
    for i in range(len(allgemeinerVerbindungsvektor)):
        sum += allgemeinerVerbindungsvektor[i] * Vektor2[i]
    equation = sp.Eq(0, sum)
    solution = sp.solve(equation)[0]
    return float(sp.solve(equation)[0])


def punkt_aus_gerade_und_parameter(gerade: Gerade, parameter: float) -> Point:
    t = sp.symbols('t')
    vec = []
    for i in range(len(gerade.sv)):
        vec.append(gerade.sv[i] + parameter * gerade.rv[i])
    return Point(len(vec), vec)


def skalarprodukt(vektor1, vektor2):
    sum = 0
    for i in range(len(vektor1)):
        sum += vektor1[i]*vektor2[i]
    return sum


def lotfusspunkt_aus_ebene_und_gerade(ebene: Layer, g: Gerade):
    t = sp.symbols('t')
    equation_string = 0
    for i in range(len(g.sv)):
        equation_string += (ebene.normalenvektor[i] * (g.sv[i] + g.rv[i] * t))
    equation = sp.Eq(equation_string, ebene.number)
    par = float(sp.solvers.solve(equation)[0])
    if isinstance(g.sv, tuple):
        g.sv = g.sv[0]
    return punkt_aus_gerade_und_parameter(g, par)


def check_lagebeziehung(gerade1: Gerade, gerade2: Gerade):
    r = sp.symbols('r')
    s = sp.symbols('s')
    g1_equations = []
    g2_equations = []
    for i in range(len(gerade1.rv)):
        g1_equations.append(r*gerade1.rv[i])
        g2_equations.append(gerade2.rv[i])
    solved_equations = []
    for i in range(len(g1_equations)):
        equation = sp.Eq(g1_equations[i], g2_equations[i])
        solved_equations.append(sp.solvers.solve(equation))
    if all(x == solved_equations[0] for x in solved_equations):
        return "parallel oder identisch"
    else:
        solved_equations = []
        new_equations = []
        for equation in solved_equations:
            new_equations.append(sp.Eq(r, equation[r]))
        solutions = sp.solve(new_equations, [r, s])
        if len(solutions) == 0:
            return "windschief"
        else:
            punkt = punkt_aus_gerade_und_parameter(gerade1, float(solutions[r]))
            return f"schneidend {punkt.output()}"

if __name__ == "__main__":
    toCalc = checkWantedCalculation()
    if toCalc["punkte"] + toCalc["geraden"] + toCalc["ebenen"] > 2:
        print("Es können nur Abstände zwischen Punkten, Ebenen und Geraden berechnet werden. Mehr als zwei angaben (z.B. zwei Punkte) ist nicht möglich")
        sys.exit()
    elif toCalc["punkte"] == 2:
        # Abstand zwischen zwei Punkten
        p1 = Point(info="Gib die Koordinaten des ersten Punktes durch Kommas getrennt ein und drücke dann die Eingabetaste.\n1. Point: ")
        p2 = Point(info="\nJetzt die des zweiten Punktes: \n2. Point: ")
        v = verbindungsvektor(p1, p2)
        d = beautify(vektorLänge(v))
        print(f"\nAbstand: {d} LE")
    elif toCalc["punkte"] == 1:
        p = Point(info="Gib die Koordinaten des Punktes durch Kommas getrennt ein und drücke dann die Eingabetaste.\nPunkt: ")
        if toCalc["geraden"] == 1:
            # Abstand zwischen Point und Gerade
            g = Gerade(info="\nGib jetzt die Koordinaten der Geraden ein")
            pg: list = allg_verb_vek_p_g(p, g)  # Allgemeinen Verbindungsvektor aus dem eingegebenen Point und der Geraden berechnen
            par = float(parameter_orthogonal_punkt_gerade(pg, g.rv))  # Den Parameter für die Gerade berechnen, für den Point mit dem geringsten Abstand
            punkt: Point = punkt_aus_gerade_und_parameter(g, par)  # Den Point auf der Geraden berechnen, der am nächsten an dem Point dran ist
            verbindungsvektor = verbindungsvektor(p, punkt)
            abstand = vektorLänge(verbindungsvektor)
            print(f"\nParameter der Geraden: {beautify(par)}")
            print(f"Nächster Point auf der Geraden: {punkt.output()}")
            print(f"Abstand: {beautify(abstand)} LE")
        if toCalc["ebenen"] == 1:
            # Abstand zwischen Point und Layer
            e = Layer()
            hilfsgerade = hilfsgerade(e.normalenvektor, p)
            lotfusspunkt = lotfusspunkt_aus_ebene_und_gerade(e, hilfsgerade)
            print(f"\nLotfußpunkt: {lotfusspunkt.output()}")
            abstand = vektorLänge(verbindungsvektor(p, lotfusspunkt))
            print(f"Abstand: {beautify(abstand)} LE")

    elif toCalc["punkte"] == 0:
        if toCalc["geraden"] == 2:
            # Abstand zwischen zwei Geraden
            g1 = Gerade(info="Gib die Koordinaten der ersten Geraden durch Kommas getrennt ein und drücke dann die Eingabetaste")
            g2 = Gerade(info="\nJetzt die zweite Gerade:")
            lagebeziegung = check_lagebeziehung(g1, g2)
            if lagebeziegung == "parallel oder identisch":
                p = Point(number_of_coordinates=len(g1.sv), liste_der_Koordinaten=g1.sv)  # Aufpunkt der Gerade 1
                allgemeiner_verbindungsvektor = allg_verb_vek_p_g(p, g2)  # Allgemeiner Verbindungsvektor zwischen diesem Point und der Geraden 2
                par = parameter_orthogonal_punkt_gerade(allgemeiner_verbindungsvektor, g2.rv)  # Parameter für geringsten Abstand berechnen
                closest_point = punkt_aus_gerade_und_parameter(g2, par)
                verbindungsvektor = verbindungsvektor(p, closest_point)
                abstand = vektorLänge(verbindungsvektor)
                if abstand == 0.0:
                    print(f"Abstand: 0, die Geraden sind identisch")
                else:
                    print(f"Abstand: {beautify(abstand)}")
            elif "schneidend" in lagebeziegung:
                print(f"\nAbstand: 0, die geraden schneiden sich im Point {lagebeziegung.replace('schneidend ', '')}")
            elif lagebeziegung == "windschief":
                allgemeiner_verbindungsvektor = allg_verb_vek_g_g(g1, g2)
                eq1 = skalarprodukt(allgemeiner_verbindungsvektor, g1.rv)
                r, s = sp.symbols('r s')
                eq2 = skalarprodukt(allgemeiner_verbindungsvektor, g2.rv)
                solutions = sp.solve([eq1, eq2], [r, s])
                punkt_g1 = punkt_aus_gerade_und_parameter(g1, float(solutions[r]))
                punkt_g2 = punkt_aus_gerade_und_parameter(g2, float(solutions[s]))

                verbindungsvektor = verbindungsvektor(punkt_g2, punkt_g1)
                abstand = vektorLänge(verbindungsvektor)

                if abstand == 0.0:
                    print(f"\nAbstand: 0, die Geraden schneiden sich in im Point {punkt_g1.output()}, da ihre Aufpunkte identisch sind.")
                else:
                    print(f"\nNächster Point auf 1. Gerade: {punkt_g1.output()}")
                    print(f"Nächster Point auf 2. Gerade: {punkt_g2.output()}")
                    print(f"Abstand: {beautify(abstand)} LE")

        elif toCalc["geraden"] == 1:
            if toCalc["ebenen"] == 1:
                # Abstand zwischen einer Geraden und einer Layer
                g = Gerade(info="Gib die Koordinaten der Geraden durch Kommas getrennt ein und drücke dann die Eingabetaste ")
                e = Layer(info="\nWähle jetzt die Form, in der die Layer gegeben ist: ")
                hilfspunkt = Point(number_of_coordinates=len(g.sv), liste_der_Koordinaten=g.sv)
                hilfsgerade = hilfsgerade(e.normalenvektor, hilfspunkt)
                lotfusspunkt = lotfusspunkt_aus_ebene_und_gerade(e, hilfsgerade)
                print(f"\nLotfußpunkt: {lotfusspunkt.output()}")
                abstand = vektorLänge(verbindungsvektor(hilfspunkt, lotfusspunkt))
                print(f"Abstand: {beautify(abstand)} LE")
        elif toCalc["ebenen"] == 2:
            # Abstand zwischen zwei Ebenen
            e1 = Layer(info="In welcher Form ist die erste Layer gegeben?")
            e2 = Layer(info="\nIn welcher Form ist die zweite Layer gegeben?")
            if kollinear(e1.normalenvektor, e2.normalenvektor) == False:
                print("Abstand: 0, die Ebenen schneiden sich")
            else:
                x1 = sp.symbols('x1')
                equation = sp.Eq(e1.number, e1.normalenvektor[0]*x1)
                parameter_spurpunkt_x1 = float(sp.solve(equation)[0])
                x1_achse = Gerade(sv=[0.0, 0.0, 0.0], rv=[1.0, 0.0, 0.0])
                spurpunkt_x1 = punkt_aus_gerade_und_parameter(x1_achse, parameter_spurpunkt_x1)

                hilfsgerade = hilfsgerade(e1.normalenvektor, spurpunkt_x1)
                lfp = lotfusspunkt_aus_ebene_und_gerade(e2, hilfsgerade)
                abstand = vektorLänge(verbindungsvektor(lfp, spurpunkt_x1))
                if abstand == 0:
                    print(f"\nAbstand: 0 LE, die Ebenen sind identisch.")
                else:
                    print(f"\nAbstand: {beautify(abstand)} LE")
