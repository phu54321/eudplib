import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap_multiplay.scx')


@EUDFunc
def main():
    if EUDInfLoop():
        f_setcurpl(Player2)
        Trigger(
            ElapsedTime(AtLeast, 3),
            Defeat()
        )
        EUDDoEvents()
    EUDEndInfLoop()


SaveMap('outputmap/testmultiplay.scx', main)
