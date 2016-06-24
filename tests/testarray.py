import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    k = EUDArray(10)
    n = EUDVariable(Addr(k))
    b = EUDVariable()
    b << n
    a = EUDArray(b)
    for i in range(10):
        a.set(i, 2 ** i)

    for i in range(10):
        f_simpleprint(a.get(i) + 10)

SaveMap('outputmap\\testarray.scx', main)
