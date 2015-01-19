#cython: boundscheck=False

cdef int* cargs = [
    0x08D3DCB1,
    0x05F417D1,
    0x01886E5F,
    0x01539095,
    0x00980E41,
    0x006D0B81,
    0x0060CDB5,
    0x0059686D,
    0x0045A523,
    0x0041BBB3,
]

def verifyf(unsigned char* buf, int buflen):
    cdef unsigned int i, j, compv, count, idx, carg, dw

    counts = [0] * 10

    for idx in range(10):
        carg = cargs[idx]

        compv = 12345 * carg
        count = 0
        for j in range(0, buflen, 4):
            dw = (
                (buf[j + 0] << 0) |
                (buf[j + 1] << 8) |
                (buf[j + 2] << 16) |
                (buf[j + 3] << 24)
            )

            if dw >= compv:
                count += 1
            compv = compv + carg
        counts[idx] = count

    return counts
