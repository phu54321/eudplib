import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))


from eudplib import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def f_add(a, b):
    return a + b


@EUDFunc
def f_mul(a, b):
    return a * b


@EUDFunc
def f_div(a, b):
    return a // b, a % b


@EUDFunc
def f_addmul(a, b):
    return a + b, a * b


@EUDFunc
def testnoret():
    f_simpleprint('Test function')
    DoActions(DisplayText('Tello'))


@EUDFunc
def main():
    p = EUDFuncPtr(2, 1)

    # Test - Simple pattern
    p << f_add
    a = p(7, 9)

    p << f_mul
    b = p(7, 9)

    try:
        p << f_div  # Should trigger error
    except EPError as e:
        print(' - Error as expected : %s' % e)

    f_simpleprint(a, b)  # 16 63

    # Test2 - multi return
    q = EUDFuncPtr(2, 2, f_div)
    a1, a2 = q(12, 5)
    q << f_addmul
    b1, b2 = q(12, 5)
    q << f_div
    c1, c2 = q(17, 3)
    f_simpleprint(a1, a2, b1, b2, c1, c2)  # 2 2 17 60 5 2

    # Test 3 - no arg no ret
    r = EUDFuncPtr(0, 0, testnoret)
    r()


SaveMap('outputmap/testfptr.scx', main)
