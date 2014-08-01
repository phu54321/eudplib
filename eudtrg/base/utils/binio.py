
"""
Simple integer <-> bytes conversion. Used internally in eudtrg.
"""

from eudtrg import LICENSE  # @UnusedImport


def i2b4(i):
    return bytes((
        0xFF & i,
        0xFF & (i >> 8),
        0xFF & (i >> 16),
        0xFF & (i >> 24)
    ))


def i2b2(i):
    return bytes((
        0xFF & i,
        0xFF & (i >> 8)
    ))


def i2b1(i):
    return bytes([
        0xFF & i
    ])


def b2i1(b, index):
    return b[index]


def b2i2(b, index):
    return (b[index] +
            (b[index + 1] << 8))


def b2i4(b, index):
    return ((b[index]) +
            (b[index + 1] << 8) +
            (b[index + 2] << 16) +
            (b[index + 3] << 24))
