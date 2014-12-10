#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from .. import core as c


class EUDVarBuffer(c.EUDObject):
    """Variable buffer

    40 bytes per variable.
    """

    def __init__(self):
        super().__init__()

        self._varn = 0

    def CreateVarTrigger(self):
        ret = self + (60 * self._varn)
        self._varn += 1
        return ret

    def GetDataSize(self):
        return 2408 + 60 * (self._varn - 1)

    def WritePayload(self, emitbuffer):
        output = bytearray(2408 + 60 * (self._varn - 1))

        for i in range(self._varn):
            # 'preserve trigger'
            output[60 * i + 2376:60 * i + 2380] = b'\x04\0\0\0'

        emitbuffer.WriteBytes(output)


_evb = None


def RegisterNewVariableBuffer():
    global _evb
    _evb = EUDVarBuffer()


def GetCurrentVariableBuffer():
    return _evb


c.RegisterCreatePayloadCallback(RegisterNewVariableBuffer)
