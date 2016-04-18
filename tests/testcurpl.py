import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    i = EUDVariable()
    j = EUDVariable()
    for v in EUDLoopRange(10):
        j += v
    f_setcurpl(Player2)
    a = f_getcurpl()
    f_setcurpl(Player5)
    b = f_getcurpl()
    DoActions(SetMemory(0x6509B0, SetTo, 5))
    c = f_getcurpl()
    f_setcurpl(Player1)
    f_simpleprint("Should be 145, ", a, b, c, " ", i, " ", j)


SaveMap('outputmap\\testcurpl.scx', main)
