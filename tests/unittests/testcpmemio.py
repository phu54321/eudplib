from helper import *


@TestInstance
def test_cpmemio():
    a = Db(i2b4(0x1234) + i2b4(0x5678) + i2b4(0x9abc))

    f_setcurpl(EPD(a))

    # Normal reading
    ptr, epd = f_dwepdread_cp(0)
    test_equality(
        'f_dwread_cp with cpo=0',
        [ptr, 0x58A364 + 4 * epd],
        [0x1234, 0x1234]
    )

    a, b, c = (
        f_dwread_cp(0),
        f_dwread_cp(1),
        f_dwread_cp(2),
    )

    test_equality(
        'f_dwread_cp',
        [a, b, c], [0x1234, 0x5678, 0x9abc]
    )

    # Issue #4: This should at least compile.
    v = EUDVariable(0)
    f_dwepdread_cp(v)

    # Writing
    f_dwwrite_cp(1, 0x1111)
    a, b, c = (
        f_dwread_cp(0),
        f_dwread_cp(1),
        f_dwread_cp(2),
    )

    test_equality(
        'f_dwread_cp',
        [a, b, c], [0x1234, 0x1111, 0x9abc]
    )

    f_setcurpl(P1)
