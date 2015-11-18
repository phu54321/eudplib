import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    # VMixed actions
    a = EUDVariable()

    a << 0
    DoActions(SetDeaths(a, SetTo, EPD(a), 0))
    a << 1
    DoActions(SetDeaths(a, SetTo, f_mul(a, 30), 0))
    a << 2
    DoActions(SetDeaths(a, SetTo, a - 50, 0))
    DoActions([
        SetDeaths(3, SetTo, 123, 0),
        SetDeaths(a, SetTo, a, a)
    ])


SaveMap('outputmap/testexttrig.scx', main)
