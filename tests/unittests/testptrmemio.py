from helper import *


@TestInstance
def test_ptrmemio():
    a = Db(b'\x01\x02\x03\x04\x05\x06\x07\x08')

    # bread
    f_setcurpl(Player1)
    cp0 = f_getcurpl()
    br0 = f_bread(a + 0)
    cp1 = f_getcurpl()
    br1 = f_bread(a + 3)
    cp2 = f_getcurpl()
    test_equality(
        'f_bread',
        [cp0, br0, cp1, br1, cp2],
        [0, 1, 0, 4, 0]
    )

    # wread
    f_setcurpl(Player1)
    cp0 = f_getcurpl()
    wr0 = f_wread(a + 0)
    cp1 = f_getcurpl()
    wr1 = f_wread(a + 1)
    cp2 = f_getcurpl()
    wr2 = f_wread(a + 3)
    cp3 = f_getcurpl()
    test_equality(
        'f_wread',
        [cp0, wr0, cp1, wr1, cp2, wr2, cp3],
        [0, 0x0201, 0, 0x0302, 0, 0x0504, 0]
    )

    # dwread
    f_setcurpl(Player1)
    cp0 = f_getcurpl()
    dwr0 = f_dwread(a + 0)
    cp1 = f_getcurpl()
    dwr1 = f_dwread(a + 1)
    cp2 = f_getcurpl()
    dwr2 = f_dwread(a + 3)
    cp3 = f_getcurpl()
    test_equality(
        'f_dwread',
        [cp0, dwr0, cp1, dwr1, cp2, dwr2, cp3],
        [0, 0x04030201, 0, 0x05040302, 0, 0x07060504, 0]
    )
