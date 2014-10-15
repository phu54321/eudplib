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
scenario.chk section tokenizer. Internally used in eudtrg.
'''

import struct
from ..utils import ubconv
from ..utils import binio

# conversion from string to ulong.
#  ex) TYPE -> 54 59 50 45 -> 0x45505954 -> 1162893652
#


def string2ulong(s):
    # s may be string or bytes. convert to bytes.
    if type(s) is str:
        s = ubconv.u2b(s)

    if len(s) < 4:
        ts = s
        s = [32] * 4  # 32 is ' ' (space). ex) 'VER' translates to 'VER '
        s[0:len(ts)] = ts

    return binio.b2i4(s, 0)


"""
General CHK class.
"""


class CHK:

    def __init__(self):
        self.sections = {}

    def loadblank(self):
        self.sections = {}

    def loadchk(self, b):
        # this code won't handle protection methods properly such as...
        #  - duplicate section name
        #  - jump section protection
        #
        # this program although handles
        #  - invalid section length (too high)
        #  - unused sections

        t = self.sections  # temporarilly store
        self.sections = {}

        try:
            index = 0
            while 1:
                # read data
                sectionname = binio.b2i4(b, index)
                sectionlength = binio.b2i4(b, index + 4)

                if sectionlength < 0:
                    # jsp with negative section size.
                    # jsp are not supported. Supporting them is boring.
                    return False

                section = b[index + 8: index + 8 + sectionlength]
                index += sectionlength + 8

                # This code won't handle sections with same sectionname.
                self.sections[sectionname] = section
                # Just overwrite. We're not making another unprotector.

            return True

        except RuntimeError:
            # read failed. unsupported chk protection method applied.
            self.section = t
            return False

        except IndexError:
            return True  # read completed

    def savechk(self):
        # calculate output size
        blist = []
        for name, binary in self.sections.items():
            blist.append(
                b''.join([struct.pack('<LL', name, len(binary)), binary]))

        return b''.join(blist)

    def enumsection(self):
        return list(self.sections.keys())

    def getsection(self, sectionname):
        sectionname = string2ulong(sectionname)
        return self.sections[sectionname]  # Nameerror may be raised.

    def setsection(self, sectionname, b):
        sectionname = string2ulong(sectionname)
        self.sections[sectionname] = bytes(b)

    def delsection(self, sectionname):
        sectionname = string2ulong(sectionname)
        del self.sections[sectionname]

    def optimize(self):

        # Delete unused sections
        used_section = [string2ulong(name) for name in
                        [
            'VER', 'VCOD', 'OWNR', 'ERA', 'DIM', 'SIDE', 'MTXM', 'UNIT',
            'THG2', 'MASK', 'STR', 'UPRP', 'MRGN', 'TRIG', 'MBRF', 'SPRP',
            'FORC', 'COLR', 'PUNI', 'PUPx', 'PTEx', 'UNIx', 'UPGx', 'TECx',
        ]]

        unused_section = [
            sn for sn in self.sections.keys() if sn not in used_section]
        for sn in unused_section:
            del self.sections[sn]

        # Terrain optimization
        dim = self.getsection('DIM')
        mapw = binio.b2i2(dim, 0)
        maph = binio.b2i2(dim, 2)
        terrainsize = mapw * maph

        # MASK optimization : cancel 0xFFs.
        mask = self.getsection('MASK')
        clippos = 0
        for i in range(terrainsize - 1, -1, -1):
            if mask[i] != 0xff:
                clippos = i + 1
                break

        mask = mask[:clippos]
        self.setsection('MASK', mask)

        # MTXM optimization
        # MASK optimization : cancel 0xFFs.
        mtxm = self.getsection('MTXM')
        clippos = 0
        for i in range(terrainsize - 1, -1, -1):
            if mtxm[2 * i] != 0x00 or mtxm[2 * i + 1] != 0x00:
                clippos = i + 1
                break

        mtxm = mtxm[:2 * clippos]
        self.setsection('MTXM', mtxm)

        # More optimization would be possible, but I don't care.
