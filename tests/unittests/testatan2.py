from helper import *


@TestInstance
def test_atan2():
    atanarray = EUDArray(360)
    for angle in EUDLoopRange(360):
        x, y = f_lengthdir(1000, angle)
        atanarray[angle] = f_atan2(y, x)

    # Value of atan2 may vary by 1 due to rounding error.
    # Here we check similarity.
    test_assert(
        "atan2 test",
        [atanarray[angle] - angle + 1 <= 2 for angle in range(360)]
    )
