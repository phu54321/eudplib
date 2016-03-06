import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def multest():
    a, b, c = EUDCreateVariables(3)
    a << 200000
    b << 1
    c << 1

    if EUDWhile()(a >= 1):
        a -= 1
        b += 1
        c << c * b + 3
    EUDEndWhile()


def perftest(funcname, func):
    starttm = f_dwread_epd(EPD(0x51CE8C))
    DoActions(SetMemory(0x6509A0, SetTo, 0))  # EUD Turbo
    func()
    EUDDoEvents()
    endtm = f_dwread_epd(EPD(0x51CE8C))
    f_simpleprint("[%s] Elapsed time : " % funcname, starttm - endtm)


@EUDFunc
def main():
    EUDDoEvents()

    perftest("multest", multest)


SaveMap('outputmap/perfest.scx', main)
