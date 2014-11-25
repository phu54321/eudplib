import struct
from . import scaddr
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
        number = scaddr.Evaluate(number)
        assert number.offset_applied == 0, 'Non-constant given.'
        number.number &= 0xFF

        self._datas.append(binio.i2b1(number.number))
        self._datalen += 1

    def EmitWord(self, number):
        number = scaddr.Evaluate(number)
        assert number.offset_applied == 0, 'Non-constant given.'
        number.number &= 0xFFFF

        self._datas.append(binio.i2b2(number.number))
        self._datalen += 2

    def EmitDword(self, number):
        number = scaddr.Evaluate(number)
        number.number &= 0xFFFFFFFF

        if number.offset_applied:
            self._tablebr[number.offset_applied].append(self._datalen)

        self._datas.append(binio.i2b4(number.number))
        self._datalen += 4

    def EmitPack(self, structformat, *arglist):
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

        evals = [scaddr.Evaluate(arg) for arg in arglist]
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
