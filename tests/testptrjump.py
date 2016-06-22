import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    a = EUDVariable()
    t = Forward()

    a << t
    EUDJump(t)

    DoActions(DisplayText('Hello World!'))
    t << NextTrigger()
    DoActions(DisplayText('After jump'))

SaveMap('outputmap/testptrjump.scx', main)
