'''
Defines class EUDGrp.
'''

from eudtrg.base import *
from eudtrg.baselib import *

import struct

class EUDGrp(EUDObject):
    '''
    Object wrapper for GRP
    '''

    def __init__(self, content):
        super().__init__()
        self._content = content

    def EvalImpl(self):
        return super().EvalImpl() + 2 # 2 padding bytes.


    def GetDependencyList(self):
        return []

    def GetDataSize(self):
        return len(self._content) + 2

    def WritePayload(self, buf):
        buf.EmitBytes(b'\0\0') # 2byte padding to align dwords at (*)

        # fill in grp header
        b = self._content
        fn, w, h = struct.unpack('<HHH', b[0:6])
        buf.EmitWord(fn)
        buf.EmitWord(w)
        buf.EmitWord(h)

        # fill in grp frame headers table
        selfaddr = self.Evaluate() # Evaluate itself : Get address of itself.

        for i in range(fn):
            fhoffset = 6 + 8*i
            xoff, yoff, w, h, lto = struct.unpack('<BBBBI', b[fhoffset : fhoffset + 8])
            buf.EmitByte(xoff)
            buf.EmitByte(yoff)
            buf.EmitByte(w)
            buf.EmitByte(h)
            buf.EmitDword(lto + selfaddr) # (*)

        buf.EmitBytes(b[6+8*fn:])
