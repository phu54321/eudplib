#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct

from . import scaddr, rlocint
from ..utils import binio


class Payload:
    def __init__(self, data, prttable, orttable):
        self.data = data
        self.prttable = prttable
        self.orttable = orttable


_packerlist = {}


class PayloadBuffer:
    '''
    Buffer where EUDObject should write to.
    '''

    def __init__(self, totlen):
        self._data = bytearray(totlen)
        self._totlen = totlen

        self._prttable = []
        self._orttable = []

    def StartWrite(self, writeaddr):
        self._datastart = writeaddr
        self._datacur = writeaddr

    def EndWrite(self):
        return self._datacur - self._datastart

    def WriteByte(self, number):
        number = scaddr.Evaluate(number)
        assert number.rlocmode == 0, 'Non-constant given.'
        number.offset &= 0xFF

        self._data[self._datacur] = binio.i2b1(number.offset)
        self._datacur += 1

    def WriteWord(self, number):
        number = scaddr.Evaluate(number)
        assert number.rlocmode == 0, 'Non-constant given.'
        number.offset &= 0xFFFF

        self._data[self._datacur: self._datacur + 2] = binio.i2b2(number.offset)
        self._datacur += 2

    def WriteDword(self, number):
        number = scaddr.Evaluate(number)
        number.offset &= 0xFFFFFFFF

        if number.rlocmode:
            assert self._datacur % 4 == 0, 'Non-const must be aligned to 4byte'
            if number.rlocmode == 1:
                self._prttable.append(self._datacur)
            elif number.rlocmode == 4:
                self._orttable.append(self._datacur)
            else:
                raise AssertionError('rlocmode should be 1 or 4')

        self._data[self._datacur: self._datacur + 4] = binio.i2b4(number.offset)
        self._datacur += 4

    def WritePack(self, structformat, *arglist):
        '''
        ======= =======
          Char   Type
        ======= =======
           B     Byte
           H     Word
           I     Dword
        ======= =======
        '''

        if structformat not in _packerlist:
            _packerlist[structformat] = _CreateStructPacker(structformat)

        _packerlist[structformat](self, *arglist)

    def WriteBytes(self, b):
        '''
        Write bytes object to buffer.

        :param b: bytes object to write.
        '''
        b = bytes(b)
        self._data[self._datacur: self._datacur + len(b)] = b
        self._datacur += len(b)

    def WriteSpace(self, spacesize):
        self._datacur += spacesize

    # Internally used
    def CreatePayload(self):
        return Payload(bytes(self._data), self._prttable, self._orttable)


def _CreateStructPacker(structformat):
    sizedict = {'B': 1, 'H': 2, 'I': 4}
    anddict = {'B': 0xff, 'H': 0xffff, 'I': 0xffffffff}

    dataoffsetlist = []
    andvallist = []
    sizelist = []

    structlen = 0

    for s in structformat:
        datasize = sizedict[s]
        dataoffsetlist.append(structlen)
        structlen += datasize

        andvallist.append(anddict[s])
        sizelist.append(datasize)

    def packer(buf, *arglist):
        dpos = buf._datacur

        evals = [scaddr.Evaluate(arg) for arg in arglist]
        for i, ri in enumerate(evals):
            assert type(ri) is rlocint.RlocInt
        evalnum = [ri.offset & andvallist[i] for i, ri in enumerate(evals)]

        # 1. Add binary data
        packed = struct.pack(structformat, *evalnum)
        buf._data[dpos: dpos+len(packed)] = packed

        # 2. Update relocation table
        for i, ri in enumerate(evals):
            assert (ri.rlocmode == 0 or
                    (sizelist[i] == 4 and dataoffsetlist[i] % 4 == 0)), (
                'Cannot write non-const in byte/word/nonalligned dword.'
            )

            if ri.rlocmode == 1:
                buf._prttable.append(dpos + dataoffsetlist[i])

            elif ri.rlocmode == 4:
                buf._orttable.append(dpos + dataoffsetlist[i])

        buf._datacur += structlen

    return packer
