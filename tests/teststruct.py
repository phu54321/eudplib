import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


class TestStruct(EUDStruct):
    _fields_ = ['x', 'y']


@EUDFunc
def main():
    a = TestStruct()
    a.x = 5
    a.y = 7

    b = TestStruct(a.addr())
    c = TestStruct(b.addr())
    d = TestStruct(c.addr())

    c.x = 3

    f_simpleprint(d.x, d.y)

SaveMap('outputmap\\teststruct.scx', main)
