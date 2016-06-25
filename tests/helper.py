# TEST HELPER

import sys as _sys
import os as _os

_sys.path.insert(0, _os.path.abspath('..\\'))

from eudplib import *


def test_assert(testname, condition):
    if EUDIf()(condition):
        f_simpleprint("\x07[ OK ] \x04%s" % testname)
    if EUDElse()():
        f_simpleprint("\x08[FAIL] \x04%s" % testname)
    EUDEndIf()

    DoActions([SetMemory(0x6509A0, SetTo, 0)])
