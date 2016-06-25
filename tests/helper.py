# TEST HELPER

import sys as _sys
import os as _os

_sys.path.insert(0, _os.path.abspath('..\\'))

from eudplib import *


_testing = EUDVariable()
_failedTest = EUDArray(1024)
_testNum = EUDVariable()
_failedNum = EUDVariable()


def test_assert(testname, condition):
    global _failedNum, _testNum

    if EUDIf()(condition):
        f_simpleprint("\x07[ OK ] \x04%s" % testname)
    if EUDElse()():
        f_simpleprint("\x08[FAIL] \x04%s" % testname)
        failedTestDb = DBString(testname)
        _failedTest[_failedNum] = failedTestDb
        _failedNum += 1
    EUDEndIf()

    _testNum += 1

    DoActions([SetMemory(0x6509A0, SetTo, 0)])
    EUDDoEvents()


def test_complete():
    f_simpleprint("\x03" + "=" * 40)
    succNum = _testNum - _failedNum
    f_simpleprint("\x04  Test result : ", succNum, "/", _testNum, spaced=False)

_testList = []


def TestInstance(func):
    _testList.append(func)
    return func


@EUDFunc
def _testmain():
    for _test in _testList:
        _test()

    test_complete()


def test_runall():
    LoadMap("outputmap/basemap/basemap.scx")
    SaveMap("outputmap/testall.scx", _testmain)
