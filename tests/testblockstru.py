import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    if EUDInfLoop():
        f_setcurpl(Player1)
        DoActions(DisplayText("test a"))
        DoActions(DisplayText("test b"))
        DoActions(DisplayText("test c"))
        EUDDoEvents()
    EUDEndInfLoop()


SaveMap('outputmap\\blockstru.scx', main)
