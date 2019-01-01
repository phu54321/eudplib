from helper import *


@TestInstance
def test_bitwise():
    test_equality(
        'f_bitand',
        f_bitand(0b1100, 0b1010),
        0b1100 & 0b1010
    )
    test_equality(
        'f_bitor',
        f_bitor(0b1100, 0b1010),
        0b1100 | 0b1010
    )
    test_equality(
        'f_bitxor',
        f_bitxor(0b1100, 0b1010),
        0b1100 ^ 0b1010
    )
    test_equality(
        'f_bitnand',
        f_bitnand(0b1100, 0b1010),
        ~(0b1100 & 0b1010) & 0xFFFFFFFF
    )
    test_equality(
        'f_bitnor',
        f_bitnor(0b1100, 0b1010),
        ~(0b1100 | 0b1010) & 0xFFFFFFFF
    )
    test_equality(
        'f_bitnxor',
        f_bitnxor(0b1100, 0b1010),
        ~(0b1100 ^ 0b1010) & 0xFFFFFFFF
    )
    test_equality(
        'f_bitnot',
        f_bitnot(0b1100),
        ~0b1100 & 0xFFFFFFFF
    )
