import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/Missile pack [PD] V3.6.2.scx')

main = NextTrigger()

f_inittrigtrg()

if EUDWhile(Always()):
    p = EUDVariable()
    p << 0
    if EUDWhile(p <= 7):
        f_exectrigtrg(p)
        p << p + 1
    EUDEndWhile()
    EUDDoEvents()
EUDEndWhile()

SaveMap('outputmap/trigtrg.scx', main)
