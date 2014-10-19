import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')

main = NextTrigger()

if EUDExecuteOnce():
    f_inittrigtrg()
EUDEndExecuteOnce()

p = EUDVariable()
p << 0
if EUDWhile(p <= 7):
    f_exectrigtrg(p)
    p << p + 1
EUDEndWhile()

SaveMap('outputmap/trigtrg.scx', main)
