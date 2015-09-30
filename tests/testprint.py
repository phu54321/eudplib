import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    f_initextstr()

    a = EUDVariable()
    b = EUDVariable()

    a << 5
    b = a * a * a * a * a

    s = DBString(1024)
    f_dbstr_print(s.GetStringMemoryAddr(), 'test ', a, ' b: ', b, ' test')
    DoActions(s.GetDisplayAction())


SaveMap('outputmap/testprint.scx', main)
