import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    i = EUDVariable()

    DoActions(SetDeaths(1, Add, 1, 0))
    if EUDInfLoop():
        x, y = mathf.f_lengthdir(400, i)

        x << x + 1024
        y << y + 1024

        SeqCompute([
            (EPD(0x58DC60 + 0), SetTo, x),
            (EPD(0x58DC60 + 4), SetTo, y),
            (EPD(0x58DC60 + 8), SetTo, x),
            (EPD(0x58DC60 + 12), SetTo, y)
        ])

        RawTrigger(
            actions=[
                CreateUnit(1, "Zerg Zergling", 1, P1),
                KillUnitAt(All, "Zerg Zergling", 1, P1)
            ]
        )

        i << i + 2
        RawTrigger(
            conditions=[i >= 360],
            actions=[i.SubtractNumber(0)]
        )

        DoActions([
            SetMemory(0x6509A0, SetTo, 0),
            SetMemory(0x629D90, SetTo, 1),
        ])
        EUDDoEvents()
    EUDEndInfLoop()


SaveMap('outputmap/testtrigmet.scx', main)
