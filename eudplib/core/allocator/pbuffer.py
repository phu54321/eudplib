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

from . import constexpr
from eudplib import utils as ut


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
        number = constexpr.Evaluate(number)
        ut.ep_assert(number.rlocmode == 0, 'Non-constant given.')
        self._data[self._datacur] = number.offset & 0xFF
        self._datacur += 1

    def WriteWord(self, number):
        number = constexpr.Evaluate(number)
        ut.ep_assert(number.rlocmode == 0, 'Non-constant given.')

        offset = number.offset
        self._data[self._datacur + 0] = offset & 0xFF
        self._data[self._datacur + 1] = (offset >> 8) & 0xFF
        self._datacur += 2

    def WriteDword(self, number):
        number = constexpr.Evaluate(number)
        number.offset &= 0xFFFFFFFF

        if number.rlocmode:
            ut.ep_assert(
                self._datacur % 4 == 0,
                'Non-const dwords must be aligned to 4byte'
            )
            if number.rlocmode == 1:
                self._prttable.append(self._datacur)
            elif number.rlocmode == 4:
                self._orttable.append(self._datacur)
            else:
                raise ut.EPError('rlocmode should be 1 or 4')

        offset = number.offset
        self._data[self._datacur + 0] = offset & 0xFF
        self._data[self._datacur + 1] = (offset >> 8) & 0xFF
        self._data[self._datacur + 2] = (offset >> 16) & 0xFF
        self._data[self._datacur + 3] = (offset >> 24) & 0xFF
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

        try:
            _packerlist[structformat](self, arglist)
        except KeyError:
            _packerlist[structformat] = _CreateStructPacker(structformat)
            _packerlist[structformat](self, arglist)

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
    packersrcList = []

    packersrcList.append("""\
def packer(buf, args):
    dpos = buf._datacur
    data = buf._data
    prttb = buf._prttable
    orttb = buf._orttable
""")

    dpos = 0

    for i, s in enumerate(structformat):
        packersrcList.append("\n    # Field %d (%s)\n" % (i, s))
        datasize = sizedict[s]
        packersrcList.append("    ri = constexpr.Evaluate(args[%s])\n" % i)

        # Check constant writing to non-aligned dword or word/byte.
        if not (datasize == 4 and dpos % 4 == 0):
            packersrcList.append("""\
    ut.ep_assert(
        ri.rlocmode == 0,
        'Cannot write non-const in byte/word/nonalligned dword.'
    )
""")
        else:
            packersrcList.append("""\
    if ri.rlocmode == 1:
        prttb.append(dpos + {dpos})
    elif ri.rlocmode == 4:
        orttb.append(dpos + {dpos})
""".format(**locals()))

        if s == 'B':
            packersrcList.append(
                "    data[dpos + %d] = ri.offset & 0xFF\n" % dpos)

        elif s == 'H':
            packersrcList.append("""\
    data[dpos + %d] = ri.offset & 0xFF
    data[dpos + %d] = (ri.offset >> 8) & 0xFF
""" % (dpos, dpos + 1))

        elif s == 'I':
            packersrcList.append("""\
    data[dpos + %d] = ri.offset & 0xFF
    data[dpos + %d] = (ri.offset >> 8) & 0xFF
    data[dpos + %d] = (ri.offset >> 16) & 0xFF
    data[dpos + %d] = (ri.offset >> 24) & 0xFF
""" % (dpos, dpos + 1, dpos + 2, dpos + 3))

        dpos += datasize

    packersrcList.append("\n    # End of packer\n")
    packersrcList.append("    buf._datacur += %d\n" % dpos)

    # Code generated.
    packersrc = "".join(packersrcList)
    retdict = {}
    exec(packersrc, globals(), retdict)
    return retdict['packer']
