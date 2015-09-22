import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')

CompressPayload(True)


@EUDFunc
def main():
    if EUDInfLoop():
        if EUDPlayerLoop():
            PTrigger(
                players=[Player1],
                actions=[
                    CreateUnit(1, 'Terran Marine', 'Anywhere', CurrentPlayer),
                    PreserveTrigger()
                ]
            )

            PTrigger(
                players=[Player1, Player7],
                actions=[
                    CreateUnit(1, 'Terran Firebat', 'Anywhere', CurrentPlayer),
                    PreserveTrigger()
                ]
            )

            PTrigger(
                players=[Force1],
                actions=[
                    CreateUnit(1, 'Terran Vulture', 'Anywhere', CurrentPlayer),
                    PreserveTrigger()
                ]
            )
        EUDEndPlayerLoop()
        EUDDoEvents()
    EUDEndInfLoop()


SaveMap('outputmap/testptrigger.scx', main)
