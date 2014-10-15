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
Implements LoadMap, SaveMap function
'''


from ..dataspec import trigger as trig

from .mapdata import (
    locnametable,
    unitnametable,
    strtable,
    uprptable,
    uprpdict
)

from ..utils import binio
from . import chktok, mpqapi
from . import injgen

# private variables
_chk = None
_mpqcontent = None


def PutDict_NoDup(d, key, value):
    if key in d:  # Duplication
        d[key] = None  # Mark as duplicate
    else:
        d[key] = value


def LoadMap(fname):
    '''
    Load template map and read various data from it.

    :param fname: Path to input map.
    '''

    print('Loading map %s' % fname)

    global _chk, _mpqcontent

    # read mpq content. The file will be copied to output file.
    _mpqcontent = open(fname, 'rb').read()

    # open mpq file
    mr = mpqapi.MpqRead()
    if not mr.Open(fname):
        raise RuntimeError('Failed to open map file \'%s\'.' % fname)

    # extract scenario.chk
    rawchk = mr.Extract('staredit\\scenario.chk')
    chk = chktok.CHK()
    chk.loadchk(rawchk)
    _chk = chk

    # Delete unwanted sections.
    chk.delsection('SWNM')  # Switch names are ignored in eudtrg.
    chk.delsection('UPRP')  # Unit properties are ignored here.
    chk.delsection('UPUS')  # related to uprp

    # Load STR section
    strtable.LoadData(_chk.getsection('STR'))

    # Init nametables
    locnametable.clear()
    unitnametable.clear()

    # Function for ignoring unit name color.
    def IgnoreColor(s):
        stb = []
        for ch in s:
            if 0x01 <= ch <= 0x1F or ch == 0x7F:  # Special characters.
                continue
            else:
                stb.append(bytes([ch]))

        return b''.join(stb)

    # Get location names
    mrgn = _chk.getsection('MRGN')
    if mrgn:
        locn = len(mrgn) // 20
        for i in range(locn):
            locstrid = binio.b2i2(mrgn, i * 20 + 16)
            locstr = strtable.GetString(locstrid)
            if not locstr:
                continue

            # SC counts location from 1. Weird
            PutDict_NoDup(locnametable, locstr, i + 1)

    # Get unit names
    unix = _chk.getsection('UNIx')
    if unix:
        for i in range(228):
            unitstrid = binio.b2i2(unix, 3192 + i * 2)
            unitstr = strtable.GetString(unitstrid)
            if not unitstr:
                continue

            PutDict_NoDup(unitnametable, unitstr, i)
            cignored = IgnoreColor(unitstr)
            if cignored != unitstr:
                PutDict_NoDup(unitnametable, cignored, i)

    uprptable.clear()
    uprpdict.clear()


def SaveMap(fname, root):
    '''
    Save template map with EUDObjects & various files.

    :param additionalfiles: List of (MPQ Filename, bytes) to be inserted into
        map MPQ. If different contents share the same MPQ filename, function
        will raise RuntimeError.
    '''

    print('Saving map %s' % fname)

    # write new uprp
    uprpcontent = b''.join(uprptable + [bytes(20 * (64 - len(uprptable)))])
    _chk.setsection('UPRP', uprpcontent)

    # write new str
    strcontent = strtable.SaveTBL()
    _chk.setsection('STR', strcontent)

    # Generate injector
    injgen.GenerateInjector(_chk, root)

    # optimize & dump
    _chk.optimize()
    rawchk = _chk.savechk()

    # dump mpq content and modify it
    open(fname, 'wb').write(_mpqcontent)
    mw = mpqapi.MpqWrite()
    if not mw.Open(fname, preserve_content=True):
        raise RuntimeError('Cannot open output file \'%s\'.' % _mpqcontent)

    mw.PutFile('staredit\\scenario.chk', rawchk)

    # Compact & close
    mw.Compact()
    mw.Close()
