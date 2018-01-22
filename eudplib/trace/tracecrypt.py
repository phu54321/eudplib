def T(x):
    x &= 0xFFFFFFFF
    xsq = x * x
    ret = (x * (xsq * (xsq * xsq + 1) + 1) + 0x8ada4053) & 0xFFFFFFFF
    return ret


def mix(x, y):
    return (T(x) + y + 0x10f874f3) & 0xFFFFFFFF


def unT(y):
    x = 0
    for bitindex in range(32):
        mask = (2 << bitindex) - 1
        if (y - T(x)) & mask != 0:
            x += 1 << bitindex
    return x


def unmix(z, y):
    return unT((z - 0x10f874f3 - y) & 0xFFFFFFFF)
