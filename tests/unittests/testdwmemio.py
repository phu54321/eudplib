from helper import *


@TestInstance
def test_dwmemio():
    a = Db(i2b4(0x1234))

    # Normal reading
    ptr, epd = f_dwepdread_epd(EPD(a))

    # For any ptr, there are 4 valid epd values. So comparing epd and epd
    # for equality won't work. Here we convert epd back to ptr for comparison.
    test_equality(
        'f_dwread_epd',
        [ptr, 0x58A364 + 4 * epd],
        [0x1234, 0x1234]
    )

    # epd reading for non-writable memory
    # Value at 004887C0 (code section) is EA 06 85 C0
    q = f_dwread_epd_safe(EPD(0x4887C0))
    test_equality(
        'f_dwread_epd_safe',
        q, 0xc08506ea
    )

    # Flag reading!
    f1, f2, f3, f4 = f_flagread_epd(EPD(a), 0x1000, 0x0100, ~0x0010, 0x0004)
    test_equality(
        'f_flagread_epd',
        [f1, f2, f3, f4],
        [0x1000, 0x0000, 0x1224, 0x0004]
    )

    # dwwrite
    f_dwwrite_epd(EPD(a), 1234)
    test_assert('f_dwwrite works', Memory(a, Exactly, 1234))
