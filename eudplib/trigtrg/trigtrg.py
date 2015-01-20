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

'''
WARNING! This code is speciallized for use on eudplib
- Default player of rawtrigger is 'All Player'.
- Only conditions/actions used in eudplib are declared
- Condition/Action input filtering (& 0xFFFFFFFF thing) are only applied to
  player & number section of Deaths/SetDeaths
Note this when using this code outside of eudplib.
'''

from struct import pack
from eudplib import utils as ut


def i2b1(i):
    return bytes((i & 0xFF,))


def i2b2(i):
    return bytes((i & 0xFF, (i >> 8) & 0xFF))


def i2b4(i):
    return bytes((
        i & 0xFF,
        (i >> 8) & 0xFF,
        (i >> 16) & 0xFF,
        (i >> 24) & 0xFF,
    ))


# for Deaths
AtLeast = 0
AtMost = 1
Exactly = 10

# for Set Death
SetTo = 7
Add = 8
Subtract = 9

# player enum
CurrentPlayer = 13
AllPlayers = 17

# constructor
_bc_dict = {
    1: i2b1,
    2: i2b2,
    4: i2b4,
    None: (lambda x: x)
}


def FlattenList(l):
    if type(l) is bytes or type(l) is str:
        return [l]

    try:
        ret = []
        for item in l:
            ret.extend(FlattenList(item))
        return ret

    except TypeError:  # l is not iterable
        return [l]


def Condition(locid, player, amount, unitid,
              comparison, condtype, restype, flag):
    if player < 0:
        player += 0x100000000  # EPD

    player &= 0xFFFFFFFF
    amount &= 0xFFFFFFFF

    return pack('<IIIHBBBBBB', locid, player, amount, unitid,
                comparison, condtype, restype, flag, 0, 0)


def Action(locid1, strid, wavid, time, player1,
           player2, unitid, acttype, amount, flags):
    player1 &= 0xFFFFFFFF
    player2 &= 0xFFFFFFFF

    if player1 < 0:
        player1 += 0x100000000  # EPD
    if player2 < 0:
        player2 += 0x100000000  # EPD
    return pack('<IIIIIIHBBBBBB', locid1, strid, wavid, time, player1, player2,
                unitid, acttype, amount, flags, 0, 0, 0)


def Trigger(players=[AllPlayers], conditions=[], actions=[], prtrig=True):
    conditions = FlattenList(conditions)
    actions = FlattenList(actions)

    ut.ep_assert(type(players) is list)
    ut.ep_assert(type(conditions) is list)
    ut.ep_assert(type(actions) is list)
    ut.ep_assert(len(conditions) <= 16)
    ut.ep_assert(len(actions) <= 64)
    peff = bytearray(28)
    for p in players:
        peff[p] = 1

    b = b''.join(
        conditions +
        [bytes(20 * (16 - len(conditions)))] +
        actions +
        [bytes(32 * (64 - len(actions)))] +
        [prtrig and b'\x04\0\0\0' or b'\0\0\0\0'] +
        [bytes(peff)]
    )
    ut.ep_assert(len(b) == 2400)
    return b


# conditions
def Deaths(player, comparison, number, unit):
    return Condition(
        0x00000000, player, number, unit,
        comparison, 0x0F, 0x00, 0x10)


def Memory(offset, comparison, number):
    ut.ep_assert(offset % 4 == 0)  # only this kind of comparison is possible
    player = EPD(offset)

    if 0 <= player < 12 * 228:  # eud possible
        unit = player // 12
        player = player % 12
        return Deaths(player, comparison, number, unit)

    else:  # use epd
        return Deaths(player, comparison, number, 0)


# actions
def SetDeaths(player, settype, number, unit):
    return Action(
        0x00000000, 0x00000000, 0x00000000, 0x00000000,
        player, number, unit, 0x2D, settype, 0x14)


def SetMemory(offset, settype, number):
    ut.ep_assert(offset % 4 == 0)
    player = EPD(offset)

    if 0 <= player < 12 * 228:  # eud possible
        unit = player // 12
        player = player % 12
        return SetDeaths(player, settype, number, unit)

    else:  # use epd
        return SetDeaths(player, settype, number, 0)


def DisplayTextMessage(Text):
    return Action(0, Text, 0, 0, 0, 0, 0, 9, 0, 4)


def Draw():
    return Action(0, 0, 0, 0, 0, 0, 0, 56, 0, 4)


def EPD(offset):
    ut.ep_assert(offset % 4 == 0)
    return (offset - 0x0058A364) // 4
