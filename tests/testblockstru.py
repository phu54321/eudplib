import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')

f_setcurpl(Player1)

a = EUDCreateVariables(1)
a << 1
if EUDWhile(a <= 5):
    a << a + 1
    DoActions(DisplayText("test a"))
    EUDContinueIf(a == 2)
    EUDBreakIf(a == 4)
    DoActions(DisplayText("test b"))

EUDEndWhile()


SaveMap('outputmap/blockstru.scx')
