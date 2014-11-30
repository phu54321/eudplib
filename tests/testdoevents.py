import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')

mainstart = NextTrigger()


a = EUDCreateVariables(1)
a << 1
if EUDWhile(a <= 5):
    f_setcurpl(Player1)
    DoActions(DisplayText("test a"))
    EUDContinueIf(a == 2)
    EUDBreakIf(a == 4)
    DoActions(DisplayText("test b"))

    EUDSetContinuePoint()
    a << a + 1
    EUDDoEvents()

EUDEndWhile()


SaveMap('outputmap/doevents.scx', mainstart)
