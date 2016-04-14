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

    f_simpleprint('test ', a, ' b: ', b, ' test')


SaveMap('outputmap/testprint.scx', main)
