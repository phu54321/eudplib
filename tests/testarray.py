import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    a = EUDArray(10)
    for i in range(10):
        a.set(i, 2 ** i)

    for i in range(10):
        f_dwwrite_epd(i, a.get(i) + 10)


SaveMap('outputmap\\testarray.scx', main)
