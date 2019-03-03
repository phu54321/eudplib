from helper import *


@TestInstance
def test_pvariable():
    a = PVariable([5, 5, 5, 5, 5, 5, 5, 5])
    for i in range(7):
        a[i] = 2 ** i

    for i in EUDLoopRange(2, 5):
        a[i] = i * i * i

    b = EUDVariable(a)
    c = PVariable.cast(b)

    v_sum = EUDVariable()
    n = EUDVariable(1)
    for i in EUDLoopRange(0, 8):
        v_sum += a[i] * n
        n += 1

    test_equality(
        "PVariable test",
        [v_sum, a[7]],
        [1137, 5]
    )
