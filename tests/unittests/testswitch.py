from helper import *


@TestInstance
def main():
    i = EUDVariable()
    s = EUDVariable()

    if EUDWhile()(i <= 11 - 1):
        i += 1

        EUDSwitch(i)
        if EUDSwitchCase()(7):
            s += 1

        if EUDSwitchCase()(3):
            s += 10

        if EUDSwitchCase()(4, 6):
            s += 100
            EUDBreak()

        if EUDSwitchCase()(1, 2, 5, 8):
            s += 1000
            EUDBreak()

        if EUDSwitchDefault()():
            s += 10000

        EUDEndSwitch()
    EUDEndWhile()

    test_assert("Switch test", s == 34421)
