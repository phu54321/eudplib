#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import tblformat
from ..utils import b2i2, b2i4


class StringIdMap:
    def __init__(self):
        self._s2id = {}

    def AddItem(self, string, id):
        if string in self._s2id:  # ambigious string
            self._s2id[string] = None

        else:
            self._s2id[string] = id

    def GetStringIndex(self, string):
        return self._s2id[string]


strmap = None
unitmap = None
locmap = None
swmap = None


def IgnoreColor(s):
    return ''.join(filter(lambda x: not (0x01 <= x <= 0x1F or x == 0x7F), s))


def InitStringMap(chkt):
    global strmap, unitmap, locmap, swmap

    strmap = tblformat.TBL(chkt.getsection('STR'))
    unitmap = StringIdMap()
    locmap = StringIdMap()
    swmap = StringIdMap()

    unix = chkt.getsection('UNIx')
    mrgn = chkt.getsection('MRGN')
    swnm = chkt.getsection('SWNM')

    # Get location names
    if mrgn:
        locn = len(mrgn) // 20
        for i in range(locn):
            locstrid = b2i2(mrgn, i * 20 + 16)
            locstr = strmap.GetString(locstrid)
            if locstr:
                locmap.AddItem(locstr, i)

    # Get unit names
    if unix:
        for i in range(228):
            unitstrid = b2i2(unix, 3192 + i * 2)
            unitstr = strmap.GetString(unitstrid)
            if unitstr:
                unitmap.AddItem(unitstr, i)
                unitmap.AddItem(IgnoreColor(unitstr), i)

    # Get switch names
    if swnm:
        for i in range(256):
            switchstrid = b2i4(swnm, i * 4)
            switchstr = strmap.GetString(switchstrid)
            if switchstr:
                swmap.AddItem(switchstr, i)


def GetLocationIndex(l):
    return locmap.GetStringIndex(l)


def GetStringIndex(s):
    return strmap.GetStringIndex(s)


def GetSwitchIndex(s):
    return swmap.GetStringIndex(s)


def GetUnitIndex(u):
    return unitmap.GetStringIndex(u)


def ApplyStringMap(chkt):
    chkt.setsection('STR', strmap.SaveTBL())
