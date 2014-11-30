import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    y = Forward()
    x = Trigger()
    y << Trigger(
        actions=[
            SetNextPtr(x, y)
        ]
    )

    a = EUDCreateVariables(1)
    a << 1
    if EUDWhile(a <= 5):
        DoActions(SetMemory(0x6509B0, SetTo, 0))
        DoActions(DisplayText("test a"))
        EUDContinueIf(a == 2)
        EUDBreakIf(a == 4)
        DoActions(DisplayText("test b"))

        EUDSetContinuePoint()
        a << a + 1
    EUDEndWhile()


SaveMap('outputmap/blockstru.scx', main)
