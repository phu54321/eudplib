from helper import *


@TestInstance
def test_varray():
    a = EUDVArray([5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
    for i in range(8):
        a[i] = 2 ** i

    for i in EUDLoopRange(3, 6):
        a[i] = i * i * i

    b = EUDVariable(a.addr())
    c = EUDVArray(b)

    v_sum = EUDVariable()

    for i in EUDLoopRange(0, 9):
        v_sum += c[i] * i

    test_assert("VArray test", [
        v_sum == 2292,
        a[9] == 5
    ])
