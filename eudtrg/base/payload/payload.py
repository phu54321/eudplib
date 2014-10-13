'''
Declares payload class & various helper functions. Used internally in eudtrg.
'''

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

from . import depgraph
from ..dataspec import expr
from ..utils import binio

import struct


class Payload:

    def __init__(self, data, prttable=[], orttable=[]):
        self.data = data
        self.prttable = prttable
        self.orttable = orttable


# Payload packager

def CreatePayload(root):
    needed_objects = depgraph.GetAllDependencies(root)
    objn = len(needed_objects)
    print('Collected %d objects' % objn)

    objsizetable = []
    current_cursor = 0

    # calculate addresses of all objects
    for obj in needed_objects:
        obj.SetAddress(current_cursor)

        size = obj.GetDataSize()
        objsizetable.append(size)
        size = size + (-size & 0x3)  # align by 4 byte
        current_cursor += size

    payloadsize = current_cursor

    # Write data
    buf = _PayloadBuffer()
    for i, obj in enumerate(needed_objects):
        buf.StartEmit()
        obj.WritePayload(buf)
        emitted_size = buf.EndEmit()
        assert emitted_size == objsizetable[i], \
            "Expected %d bytes, got %d bytes, Object type %s" % (
                objsizetable[i], emitted_size, str(type(obj)))
    # Reset addresses & expire expr caches
    for obj in needed_objects:
        obj.ResetAddress()

    expr.ExpireCacheToken()

    # done.
    print('Payload size = %.3fMiB' % (payloadsize / 1024 / 1024))
    return buf.CreatePayload()


# Payload buffer class related
# buffer class creates payload
_packerlist = {}


class _PayloadBuffer:

    '''
    Buffer where EUDObject should write to.
    '''

    def __init__(self):
        self._datas = []
        self._datalen = 0
        self._prttable = []
        self._orttable = []
        self._tablebr = {
            1: self._prttable,
            4: self._orttable
        }

    def StartEmit(self):
        self._datastart = self._datalen

    def EndEmit(self):
        emitted_size = self._datalen - self._datastart
        padding_byten = (-emitted_size & 0x3)
        self.EmitBytes(bytes(padding_byten))
        return emitted_size

    def EmitByte(self, number):
        '''
        Write single byte to the buffer. Byte to be written must be constant.

        :param number: Byte to put in. Automatically truncated to 0~255.
        :type number: int/:class:`Expr`
        :raises AssertionError: number is not constant.
        '''
        number = expr.Evaluate(number)
        assert number.offset_applied == 0, 'Non constant given.'
        number.number &= 0xFF

        self._datas.append(binio.i2b1(number.number))
        self._datalen += 1

    def EmitWord(self, number):
        '''
        Write single word to the buffer. Word to be written must be constant.

        :param number: Word to put in. Automatically truncated to 0~65536.
        :type number: int/:class:`Expr`
        :raises AssertionError: number is not constant.
        '''
        number = expr.Evaluate(number)
        assert number.offset_applied == 0, 'Non constant given.'
        number.number &= 0xFFFF

        self._datas.append(binio.i2b2(number.number))
        self._datalen += 2

    def EmitDword(self, number):
        '''
        Write single dword to the buffer. number may or may not be constant

        :param number: Double word to put in. Automatically truncated to
            0~4294967295.
        :type number: int/:class:`Expr`
        '''
        number = expr.Evaluate(number)
        number.number &= 0xFFFFFFFF

        if number.offset_applied:
            self._tablebr[number.offset_applied].append(self._datalen)

        self._datas.append(binio.i2b4(number.number))
        self._datalen += 4

    def EmitPack(self, structformat, *arglist):
        '''
        Write several numbers at once.

        :param structformat: Defines how to write each numbers into buffer.

            ======= =======
              Char   Type
            ======= =======
               B     Byte
               H     Word
               I     Dword
            ======= =======

            ex) 'BHI' : Byte, Word, Dword

        :param arglist: Numbers to write.


        >>> buf.EmitPack('IIBH', 0x123456, 0x7890, 0x56, 0x7891')

          -> [56 34 12 00] [90 78 00 00] [56] [91 78] is written

        '''
        if structformat not in _packerlist:
            _packerlist[structformat] = _CreateStructPacker(structformat)

        _packerlist[structformat](self, *arglist)

    def EmitBytes(self, b):
        '''
        Write bytes object to buffer.

        :param b: bytes object to write.
        '''
        b = bytes(b)
        self._datas.append(b)
        self._datalen += len(b)

    # Internally used
    def CreatePayload(self):
        return Payload(b''.join(self._datas), self._prttable, self._orttable)


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
        dlen = buf._datalen

        evals = [expr.Evaluate(arg) for arg in arglist]
        evalnum = [ri.number & andvallist[i] for i, ri in enumerate(evals)]

        # 1. Add binary data
        packed = struct.pack(structformat, *evalnum)
        buf._datas.append(packed)

        # 2. Update relocation table
        for i, ri in enumerate(evals):
            assert (ri.offset_applied == 0) or (sizelist[i] == 4)

            if ri.offset_applied == 1:
                buf._prttable.append(dlen + dataoffsetlist[i])

            elif ri.offset_applied == 4:
                buf._orttable.append(dlen + dataoffsetlist[i])

        buf._datalen += structlen

    return packer
