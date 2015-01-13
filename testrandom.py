import math

a = [
    29,
    43,
    167,
    193,
    431,
    601,
    677,
    733,
    941,
    997,
]

for n in a:
    print("0x%08X" % math.floor(4294967296 / n))
