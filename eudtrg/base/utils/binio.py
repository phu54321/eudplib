
"""
Simple integer <-> bytes conversion. Used internally in eudtrg.
"""

'''
Copyright (c) 2014 trgk

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
   3. This notice may not be removed or altered from any source
   distribution.
'''


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
