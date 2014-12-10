#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import core as c
from .. import varfunc as vf
from .. import ctrlstru as cs
from .. import stdfunc as sf


class EUDArray:
    '''
    Full variable.
    '''

    def __init__(self, len):
        self._varlist = vf.EUDCreateVariables(len)
        self._varlen = len
        self._debugstring = c.Db('[EUDArray::get] Out of bounds : %s' % hex(id(self)))

    def set(self, key, item):
        varn = self._varlen
        vlist = self._varlist

        cs.EUDSwitch(key)
        for i in range(varn):
            cs.EUDSwitchCase(i)
            vlist[i] << item
            cs.EUDBreak()

        cs.EUDSwitchDefault()
        cs.DoActions([
            c.DisplayText('[EUDArray::set] Out of bounds : %s' % self),
            c.Draw()
        ])

        cs.EUDEndSwitch()

    def set(self, key, item):
        varn = self._varlen
        vlist = self._varlist
        ret = vf.EUDVariable()

        cs.EUDSwitch(key)
        for i in range(varn):
            cs.EUDSwitchCase(i)
            ret << vlist[i]
            cs.EUDBreak()

        cs.EUDSwitchDefault()  # out of bound
        sf.f_strcpy(0x58D740, self._debugstring)
        cs.EUDJump(0)  # crash

        cs.EUDEndSwitch()
