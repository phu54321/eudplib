from helper import *

LoadMap('outputmap/basemap/basemap.scx')


@EUDFunc
def main():
    k = EUDArray(10)
    n = EUDVariable(k.addr())
    b = EUDVariable()
    b << n
    a = EUDArray(b)
    for i in range(10):
        a.set(i, 2 ** i)

    test_assert("Basic array test", [a[i] == 2 ** i for i in range(10)])

SaveMap('outputmap\\testarray.scx', main)
