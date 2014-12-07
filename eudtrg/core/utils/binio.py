#!/usr/bin/python
# -*- coding: utf-8 -*-

def b2i1(b, index=0):
    return b[index]


def b2i2(b, index=0):
    return b[index] | (b[index + 1] << 8)


def b2i4(b, index=0):
    return (
        b[index] |
        (b[index + 1] << 8) |
        (b[index + 2] << 16) |
        (b[index + 3] << 24)
    )


def i2b1(i):
    return bytes((i & 0xFF,))


def i2b2(i):
    return bytes((i & 0xFF, (i >> 8) & 0xFF))


def i2b4(i):
    return bytes((
        i & 0xFF,
        (i >> 8) & 0xFF,
        (i >> 16) & 0xFF,
        (i >> 24) & 0xFF,
    ))
