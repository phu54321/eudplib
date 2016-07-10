# TEST HELPER

import sys as _sys
import os as _os
import random as _random

_sys.path.insert(0, _os.path.abspath('..\\'))

import pyximport
pyximport.install()

from eudplib import *


_testing = EUDVariable()
_failedTest = EUDArray(1024)
_testNum = EUDVariable()
_failedNum = EUDVariable()


###############################################################
# Unit testing helpers
###############################################################


origcp = EUDVariable()


def setcp1():
    origcp << f_getcurpl()
    f_setcurpl(Player1)


def resetcp():
    f_setcurpl(origcp)


def test_assert(testname, condition):
    global _failedNum, _testNum

    setcp1()

    if EUDIf()(condition):
        f_simpleprint("\x07[ OK ] \x04%s" % testname)
        test_wait(0)
    if EUDElse()():
        f_simpleprint("\x08[FAIL] %s" % testname)
        failedTestDb = DBString(testname)
        _failedTest[_failedNum] = failedTestDb
        _failedNum += 1
        test_wait(24)
    EUDEndIf()

    resetcp()

    _testNum += 1
    test_wait(0)


def test_equality(testname, real, expt):
    global _failedNum, _testNum

    real = Assignable2List(real)
    expt = Assignable2List(expt)

    setcp1()

    if EUDIf()([r == e for r, e in zip(real, expt)]):
        f_simpleprint("\x07[ OK ] \x04%s" % testname)
        test_wait(0)
    if EUDElse()():
        f_simpleprint("\x08[FAIL] %s" % testname)
        f_simpleprint(" \x03 - \x04 Output   : ", *real)
        f_simpleprint(" \x03 - \x04 Expected : ", *expt)
        failedTestDb = DBString(testname)
        _failedTest[_failedNum] = failedTestDb
        _failedNum += 1
        test_wait(24)
    EUDEndIf()

    resetcp()

    f_setcurpl(origcp)

    _testNum += 1


def test_operator(testname, realf, exptf=None):
    if exptf is None:
        exptf = realf

    if isinstance(realf, EUDFuncN):
        f = realf._fdecl_func
    else:
        f = realf
    argcount = f.__code__.co_argcount

    @TestInstance
    def test_operator():
        inputs = [EUDVariable() for _ in range(argcount)]
        expt, real = [], []

        for i in range(20):
            rnums = [_random.randint(0, 0xFFFFFFFF) for _ in range(argcount)]
            SetVariables(inputs, rnums)
            real.append(realf(*inputs))
            expt.append(exptf(*rnums) & 0xFFFFFFFF)

        test_assert(
            "Operator test : %s" % testname,
            [r == e for r, e in zip(real, expt)]
        )


###############################################################
# Performance testing helper
###############################################################


perf_basecount = 100000


def test_perf(testname, func, count):
    starttm = f_dwread_epd(EPD(0x51CE8C))

    if EUDLoopN()(count):
        func()
    EUDEndLoopN()
    test_wait(0)

    endtm = f_dwread_epd(EPD(0x51CE8C))

    elapsedTime = starttm - endtm
    averageTime = elapsedTime // count
    setcp1()
    f_simpleprint(
        '\x03' * 150 + "[PERF] \x04%s \x03* %d    \x05" % (testname, count),
        averageTime, '/', elapsedTime, spaced=False)
    resetcp()
    test_wait(12)


###############################################################

def test_complete():
    setcp1()
    f_simpleprint("\x03" + "=" * 40)
    succNum = _testNum - _failedNum
    f_simpleprint("\x04  Test result : ", succNum, "/", _testNum, spaced=False)
    resetcp()

_testList = []


def TestInstance(func):
    print(" - Adding test instance %s" % func.__name__)
    _testList.append(func)
    return func


@EUDFunc
def _testmain():
    for _test in _testList:
        _test()

    test_complete()


def test_runall(testname):
    LoadMap("outputmap/basemap/basemap.scx")
    SaveMap("outputmap/test_%s.scx" % testname, _testmain)


def test_wait(time):
    DoActions([SetMemory(0x6509A0, SetTo, time)])
    EUDDoEvents()
