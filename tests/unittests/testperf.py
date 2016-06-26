from helper import *


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
    elapsedtime = starttm - endtm
    f_simpleprint("\x03 - \x04[%s] Elapsed time : " % funcname, elapsedtime)


@TestInstance
def test_perf():
    perftest("multest", multest)
