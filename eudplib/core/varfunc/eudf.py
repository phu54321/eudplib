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

import functools
import inspect

from .eudv import EUDVariable, SeqCompute
from ...utils import (
    FlattenList,
    List2Assignable,
    Assignable2List,
    BlockStruManager,
    SetCurrentBlockStruManager
)

from ..allocator import Forward
from .. import rawtrigger as bt


def EUDFunc(fdecl_func):
    argspec = inspect.getargspec(fdecl_func)
    assert argspec[1] is None, (
        'No variadic arguments (*args) allowed for EUDFunc.')
    assert argspec[2] is None, (
        'No variadic keyword arguments (*kwargs) allowed for EUDFunc.')

    return EUDFuncN(fdecl_func, len(argspec[0]))


class EUDFuncN:
    def __init__(self, fdecl_func, argn):
        self._argn = argn
        self._fdecl_func = fdecl_func
        functools.update_wrapper(self, fdecl_func)
        self._fstart = None
        self._fend = None
        self._fargs = None
        self._frets = None

    def CreateFuncBody(self):
        assert self._fstart is None

        f_bsm = BlockStruManager()
        prev_bsm = SetCurrentBlockStruManager(f_bsm)

        bt.PushTriggerScope()
        f_args = [EUDVariable() for _ in range(self._argn)]
        fstart = bt.NextTrigger()
        f_rets = self._fdecl_func(*f_args)
        if f_rets is not None:
            f_rets = Assignable2List(f_rets)
        fend = bt.RawTrigger()
        bt.PopTriggerScope()

        assert f_bsm.empty(), 'Block start/end mismatch inside function'
        SetCurrentBlockStruManager(prev_bsm)

        # Assert that all return values are EUDVariable.
        if f_rets is not None:  # Not void function
            for i, ret in enumerate(f_rets):
                assert isinstance(ret, EUDVariable), (
                    '#%d of returned value is not instance of EUDVariable' % i)

        self._fstart = fstart
        self._fend = fend
        self._fargs = f_args
        self._frets = f_rets

    def __call__(self, *args):
        if self._fstart is None:
            self.CreateFuncBody()

        assert len(args) == self._argn, 'Argument number mismatch'

        # Assign arguments into argument space
        SeqCompute(
            [(farg, bt.SetTo, arg) for farg, arg in zip(self._fargs, args)]
        )

        # Call body
        fcallend = Forward()

        bt.RawTrigger(
            nextptr=self._fstart,
            actions=[bt.SetNextPtr(self._fend, fcallend)]
        )

        fcallend << bt.NextTrigger()

        if self._frets is not None:
            retn = len(self._frets)
            tmp_rets = [EUDVariable() for _ in range(retn)]
            SeqCompute(
                [(tr, bt.SetTo, r) for tr, r in zip(tmp_rets, self._frets)]
            )
            return List2Assignable(tmp_rets)


def SetVariables(srclist, dstlist, mdtlist=None):
    srclist = FlattenList(srclist)
    dstlist = FlattenList(dstlist)
    assert len(srclist) == len(dstlist), 'Input/output size mismatch'

    if mdtlist is None:
        mdtlist = [bt.SetTo] * len(srclist)

    sqa = [(src, mdt, dst) for src, dst, mdt in zip(srclist, dstlist, mdtlist)]
    SeqCompute(sqa)
