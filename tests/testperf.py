import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    starttm = f_dwread_epd(EPD(0x51CE8C))
    DoActions(SetMemory(0x6509A0, SetTo, 0))

    a = EUDVariable()
    a << 200000

    if EUDWhile(a >= 1):
        a << a - 1
    EUDEndWhile()

    EUDDoEvents()

    endtm = f_dwread_epd(EPD(0x51CE8C))
    SeqCompute([(EPD(0x58a364), SetTo, starttm - endtm)])


SaveMap('outputmap/perfest.scx', main)
