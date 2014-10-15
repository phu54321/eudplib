 #!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 trgk

# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#    3. This notice may not be removed or altered from any source
#    distribution.
#
# See eudtrg.LICENSE for more info


'''
Defines class EUDGrp.
'''

from eudtrg.base import *

import struct


class EUDGrp(EUDObject):

    '''
    Object wrapper for GRP
    '''

    def __init__(self, content):
        super().__init__()
        self._content = content

    def EvalImpl(self):
        return super().EvalImpl() + 2  # 2 padding bytes.

    def GetDependencyList(self):
        return []

    def GetDataSize(self):
        return len(self._content) + 2

    def WritePayload(self, buf):
        buf.EmitBytes(b'\0\0')  # 2byte padding to align dwords at (*)

        # fill in grp header
        b = self._content
        fn, w, h = struct.unpack('<HHH', b[0:6])
        buf.EmitWord(fn)
        buf.EmitWord(w)
        buf.EmitWord(h)

        # fill in grp frame headers table
        selfaddr = self.Evaluate()  # Evaluate itself : Get address of itself.

        for i in range(fn):
            fhoffset = 6 + 8 * i
            xoff, yoff, w, h, lto = struct.unpack(
                '<BBBBI', b[fhoffset: fhoffset + 8])
            buf.EmitByte(xoff)
            buf.EmitByte(yoff)
            buf.EmitByte(w)
            buf.EmitByte(h)
            buf.EmitDword(lto + selfaddr)  # (*)

        buf.EmitBytes(b[6 + 8 * fn:])
