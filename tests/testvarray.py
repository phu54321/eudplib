import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    a = EUDVArray(10)
    for i in range(10):
        a[i] = 2 ** i

    b = EUDVariable(a)
    c = EUDVArray(b)

    for i in range(10):
        f_simpleprint(c[i])

SaveMap('outputmap\\testvarray.scx', main)
