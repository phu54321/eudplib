# chemicalFormulas.py
#
# Copyright (c) 2003, 2007, Paul McGuire
#

from pyparsing import Word, Optional, OneOrMore, Group, ParseException

# define a simple Python dict of atomic weights, with chemical symbols
# for keys
atomicWeight = {
    "O": 15.9994,
    "H": 1.00794,
    "Na": 22.9897,
    "Cl": 35.4527,
    "C": 12.0107,
    "S": 32.0655,
}

# define some strings to use later, when describing valid lists
# of characters for chemical symbols and numbers
caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowers = caps.lower()
digits = "0123456789"

# Version 1
# Define grammar for a chemical formula
# - an element is a Word, beginning with one of the characters in caps,
#   followed by zero or more characters in lowers
# - an integer is a Word composed of digits
# - an elementRef is an element, optionally followed by an integer - if
#   the integer is omitted, assume the value "1" as a default; these are
#   enclosed in a Group to make it easier to walk the list of parsed
#   chemical symbols, each with its associated number of atoms per
#   molecule
# - a chemicalFormula is just one or more elementRef's
element = Word(caps, lowers)
integer = Word(digits)
elementRef = Group(element + Optional(integer, default="1"))
chemicalFormula = OneOrMore(elementRef)

# try parsing some simple formulas
for formula in ("H2O", "NaCl", "C6H5OH", "H2SO4"):
    formulaData = chemicalFormula.parseString(formula)

    # compute molecular weight
    # - the following Python expression is a shorthand for this for loop
    #   mw = 0
    #   for sym,qty in formulaData:
    #       mw += atomicWeight[sym]*int(qty)
    mw = sum([atomicWeight[sym] * int(qty) for sym, qty in formulaData])

    # print the results
    print(formula, "->", formulaData, "(", mw, ")")

print()

# Version 2 - Auto-convert integers, and add results names


def convertIntegers(tokens):
    return int(tokens[0])

element = Word(caps, lowers)
integer = Word(digits).setParseAction(convertIntegers)
elementRef = Group(element("symbol") + Optional(integer, default=1)("qty"))
# pre-1.4.7, use this:
# elementRef = Group( element.setResultsName("symbol") + Optional( integer, default=1 ).setResultsName("qty") )
chemicalFormula = OneOrMore(elementRef)

for formula in ("H2O", "NaCl", "C6H5OH", "H2SO4"):
    formulaData = chemicalFormula.parseString(formula)

    # compute molecular weight
    mw = sum(
        [atomicWeight[element.symbol] * element.qty for element in formulaData])

    # print the results
    print(formula, "->", formulaData, "(", mw, ")")

print

# Version 3 - Compute partial molecular weight per element, simplifying
# summing
# No need to redefine grammar, just define parse action function, and
# attach to elementRef


def computeElementWeight(tokens):
    element = tokens[0]
    element["weight"] = atomicWeight[element.symbol] * element.qty

elementRef.setParseAction(computeElementWeight)


for formula in ("H2O", "NaCl", "C6H5OH", "H2SO4"):
    formulaData = chemicalFormula.parseString(formula)

    # compute molecular weight
    mw = sum([element.weight for element in formulaData])

    # print the results
    print(formula, "->", formulaData, "(", mw, ")")
