from helper import *


N = 2000
arr = EUDArray(N)


@EUDFunc
def f_bubblesort():
    for i in EUDLoopRange(N):
        for j in EUDLoopRange(N - 1 - i):
            if EUDIf()(arr[i] >= arr[i + 1]):
                t = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = t
            EUDEndIf()

    SetCurrentPlayer(P1)


@TestInstance
def test_perfbasic():
    f_srand(0)

    for i in EUDLoopRange(N):
        arr[i] = f_dwrand()

    test_perf(
        "Basic function call",
        f_bubblesort,
        1
    )
    test_perf("Basic looping", lambda: None, 100000)
