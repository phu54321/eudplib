#!/usr/bin/python
# -*- coding: utf-8 -*-

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
