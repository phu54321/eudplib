# !/usr/bin/python
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


from eudtrg.base import *  # @UnusedWildImport
from eudtrg.lib.baselib import *  # @UnusedWildImport

from .readdword import f_dwread_epd
from .memcpy import f_repmovsd

_ptrigdata = None
_ptrign = None


def f_inittrigtrg():
    global _ptrigdata, _ptrign
    # Parse triggers
    trigsection = bytearray(GetCHKSection('TRIG'))
    trign = origlen // 2400

    '''Preprocess triggers'''

    # Get trigger-executable players
    section_ownr = GetCHKSection('OWNR')
    tep = []
    for i in range(12):
        if section_ownr[i] == 0x05:
            tep.append(i)
        elif section_ownr[i] == 0x06:
            tep.append(i)

    # Get trigger forces
    forcep = ([], [], [], [])
    section_forc = GetCHKSection('FORC')
    for i in range(8):
        assert 0 <= section_forc[i] <= 3, 'Invalid FORC section'
        forcep[section_forc[i]].append(i)

    # Merge effplayer[Force%d] and effplayer[Allplayers] to effplayer[player%d]
    for i in range(trign):
        effplayer = origdata[2400-28:2400-1]
        # Trigger applied to force %d
        for f in range(4):
            if effplayer[18+f]:
                for p in forcep[f]:
                    effplayer[p] = 1

        # Trigger applied to all players
        if effplayer[17]:
            effplayer[0:8] = b'\x01'*8

        # Ignore unused players.
        for p in range(8):
            if p not in tep:
                effplayer[p] = 0

        # Erase unused portions of effplayer
        effplayer[8:27] = b'\0' * 19

        # Assign to orig.
        origdata[2400-28:2400-1] = effplayer

    # Allocate space for raw trigger data
    origdata = Db(trigsection)

    # Allocate space for triggers of each players.
    _ptrign = [0] * 8
    for i in range(trign):
        for p in range(8):
            if effplayer[p]:
                _ptrign[p] += 1

    _ptrigdata = [Db(2408 * (_ptrign[p] + 1)) for p in range(8)]

    # Create initialization trigger
    trigepd = EUDVariable(9)
    ptrigepd = [EUDVariable() for _ in range(8)]
    ptrigaddr = [EUDVariable() for _ in range(8)]

    trigepd << EPD(origdata)
    for i in range(8):
        ptrigepd[i] << EPD(_ptrigdata[i])
        ptrigaddr[i] << _ptrigdata[i]

    # Iterate through each triggers
    if EUDWhile(trigepd <= EPD(origdata + origlen)):
        # Get effplayer
        effp_a = f_dwread_epd(trigepd + 593)
        effp_b = f_dwread_epd(trigepd + 594)
        peff = [None]*8
        peff[0:4] = f_dwbreak(effp_a)[2:6]
        peff[5:8] = f_dwbreak(effp_b)[2:6]

        for p in range(8):
            if EUDIfNot(peff[p] == 0):  # Trigger is executed for player p
                ptrigaddr[p] << ptrigaddr[p] + 2408
                f_dwwrite(ptrigepd[p] + 1, ptrigaddr[p])  # nextptr
                f_repmovsd(ptrigepd[p] + 2, trigepd, 2400 // 4)  # content
                ptrigepd[p] << ptrigepd[p] + (2408 // 4)
            EUDEndIf()

        trigepd << trigepd + (2400 // 4)

    EUDEndWhile()

    # Done!


@EUDFunc
def f_exectrigtrg(player):
    endexec = Forward()

    for p in range(8):
        if EUDIf(player == p):
            ptrigstart = _ptrigdata[p]
            ptrigend = _ptrigdata[p] + 2408 * _ptrign[p]

            Trigger(
                nextptr=ptrigstart,
                actions=SetNextPtr(ptrigend, endexec)
            )

        EUDEndIf()

    endexec << NextTrigger()
