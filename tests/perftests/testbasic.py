from helper import *


@EUDFunc
def callonly():
    pass


def empty():
    pass


@TestInstance
def test_perfbasic():
    basecount = 100000

    test_perf("Basic looping", lambda: None, 100 * basecount)
    test_perf("Basic function call", EUDFunc(lambda: None), 100 * basecount)

    a, b, c, ptr = EUDCreateVariables(4)
    a << f_dwrand()
    b << f_rand()
    c << 0
    ptr << 0x58A364

    # Comparison of various functions
    test_perf("Addition", lambda: a + b, basecount)
    test_perf("Subtraction", lambda: a - b, basecount)
    test_perf("Multiplication", lambda: a * b, basecount)
    test_perf("Division", lambda: a // b, basecount)
    test_perf("f_dwread_epd", lambda: f_dwread_epd(c), basecount)
    test_perf("f_dwread_epd_safe", lambda: f_dwread_epd_safe(c), basecount)
    test_perf("f_dwbreak", lambda: f_dwbreak(a), basecount)
    test_perf("EPD", lambda: EPD(ptr), basecount)
    test_perf("f_dwread", lambda: f_dwread(ptr), basecount // 2)
    test_perf("f_bread", lambda: f_bread(ptr), basecount // 2)
