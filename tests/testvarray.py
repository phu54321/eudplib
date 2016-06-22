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

    f_simpleprint(hptr(a))

    for i in range(10):
        f_simpleprint(a[i])

SaveMap('outputmap\\testvarray.scx', main)
