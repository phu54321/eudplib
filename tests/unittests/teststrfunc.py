from helper import *


@TestInstance
def test_strbuffer():
    s = StringBuffer(1023)
    a, b, c = [PVariable() for _ in range(3)]

    s.append(hptr(a), " ", hptr(b), " ", hptr(c), "\n")

    for i in EUDLoopRange(4):
        a[i] = i
        b[i] = i * i
        c[i] = i * i * i
        s.append(i, ": a=", a[i], ", b=", b[i], ", c=", c[i], "\n")

    for j in range(4, 8):
        a[j] = j
        b[j] = j * j
        c[j] = j * j * j
        s.append(j, ": a=", a[j], ", b=", b[j], ", c=", c[j], "\n")

    f_setcurpl(P1)
    s.Display()


@TestInstance
def test_setpname():
    OptimizeSetPName()
    SetPName(P1, "dpdkfah")