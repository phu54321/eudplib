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

from ... import utils as ut
from ...trigtrg import trigtrg as tt

from .ilccompile import (
    ComputeBaseInlineCodeGlobals,
    CompileInlineCode,
)


_inlineCodes = []


def PreprocessInlineCode(chkt):
    global _inlineCodes
    trigSection = chkt.getsection('TRIG')
    _inlineCodes, trigSection = PreprocessTrigSection(trigSection)
    chkt.setsection('TRIG', trigSection)


def PreprocessTrigSection(trigSection):
    """ Fetch inline codes & compiles them """
    ComputeBaseInlineCodeGlobals()

    inlineCodes = []
    trigSegments = []
    for i in range(0, len(trigSection), 2400):
        trigSegment = trigSection[i:i + 2400]
        if len(trigSegment) != 2400:
            continue

        decoded = DecodeSpecialData(inlineCodes, trigSegment)
        if decoded:
            trigSegment = decoded

        trigSegments.append(trigSegment)

    '''
    This is rather hard to explain, but we need blank trigger.

    If inline_eudplib trigger is at the last of the trigger, then its
    nextptr should be modified to codeStart.

    But after flipprop works, RunTrigTrigger engine will re-change its nextptr
    to somewhere else, where everything quits.

    So we need 'normal' trigger at the last of TRIG triggers for every player.
    '''
    trigSegments.append(tt.Trigger(players=[tt.AllPlayers]))

    trigSection = b''.join(trigSegments)
    return inlineCodes, trigSection


def GetInlineCodeList():
    """ Get list of compiled inline_eudplib code """
    return _inlineCodes


def DecodeSpecialData(inlineCodes, trigger_bytes):
    """ Check if trigger segment has special data. """
    # Check if effplayer & current_action is empty
    for player in range(28):
        if trigger_bytes[320 + 2048 + 4 + player] != 0:
            return None

    # trg.cond[0].condtype != 0
    if trigger_bytes[15] != 0:
        return None
    # trg.act[0].acttype != 0
    if trigger_bytes[346] != 0:
        return None

    data = trigger_bytes[20:320] + trigger_bytes[352:2372]
    return ProcessInlineCode(inlineCodes, data)


def ProcessInlineCode(inlineCodes, data):
    """ Check if trigger segment has inline_eudplib code. """
    magicCode = ut.b2i4(data, 0)

    # inline_eudplib code
    if magicCode == 0x10978d4a:
        playerCode = ut.b2i4(data, 4)
        codeData = ut.b2u(data[8:]).rstrip('\0')

        # Compile code
        func = CompileInlineCode(codeData)
        funcID = len(inlineCodes) + 1024
        inlineCodes.append((funcID, func))

        # Return new trigger
        newTrigger = bytearray(2400)

        # Apply effplayer
        for player in range(27):
            if playerCode & (1 << player):
                newTrigger[320 + 2048 + 4 + player] = 1

        # Apply 4 SetDeaths
        SetDeathsTemplate = tt.SetDeaths(0, tt.SetTo, 0, 0)
        newTrigger[320 + 32 * 0: 320 + 32 * 1] = SetDeathsTemplate
        newTrigger[320 + 32 * 1: 320 + 32 * 2] = SetDeathsTemplate
        newTrigger[320 + 32 * 2: 320 + 32 * 3] = SetDeathsTemplate
        newTrigger[320 + 32 * 3: 320 + 32 * 4] = SetDeathsTemplate

        # Apply flag
        newTrigger[0:4] = ut.i2b4(funcID)
        newTrigger[2368:2372] = b'\0\0\0\x10'
        return newTrigger

    return None
