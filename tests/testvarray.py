import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    a = EUDVArray([5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
    for i in range(8):
        a[i] = 2 ** i

    for i in EUDLoopRange(3, 6):
        a[i] = i * i * i

    b = EUDVariable(a)
    c = EUDVArray(b)

    for i in EUDLoopRange(0, 8):
        f_simpleprint(c[i])

    f_simpleprint(a[9])

SaveMap('outputmap\\testvarray.scx', main)
