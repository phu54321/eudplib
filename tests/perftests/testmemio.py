from helper import *


@TestInstance
def test_perfmemio():
    c, ptr = EUDCreateVariables(2)
    c << 0
    ptr << 0x58A364
    test_perf("f_dwread_epd", lambda: f_dwread_epd(c), perf_basecount)
    test_perf("f_dwread_epd_safe", lambda: f_dwread_epd_safe(c), perf_basecount)
    test_perf("f_dwbreak", lambda: f_dwbreak(ptr), perf_basecount)
    test_perf("EPD", lambda: EPD(ptr), perf_basecount)
    test_perf("f_dwread", lambda: f_dwread(ptr), perf_basecount // 2)
    test_perf("f_bread", lambda: f_bread(ptr), perf_basecount // 2)
