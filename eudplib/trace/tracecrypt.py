def T(x):
    x &= 0xFFFFFFFF
    for i in range(4):
        xsq = x * x
        x = (x * (xsq * (xsq * xsq + 1) + 1) + 0x8ada4053) & 0xFFFFFFFF
    return x


def mix(x, y):
    return T(T(x) + y + 0x10f874f3) & 0xFFFFFFFF
