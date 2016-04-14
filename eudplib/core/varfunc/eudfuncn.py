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

from .eudv import EUDVariable, SeqCompute, SetVariables
from ...utils import (
    List2Assignable,
    Assignable2List,
)

from ...utils.blockstru import (
    BlockStruManager,
    SetCurrentBlockStruManager
)

from ..allocator import Forward
from .. import rawtrigger as bt

from eudplib import utils as ut


_currentCompiledFunc = None
_currentTriggerCount = 0


def _updateFuncTriggerCount():
    global _currentTriggerCount
    currentCounter = bt.GetTriggerCounter()
    addedTriggerCount = currentCounter - _currentTriggerCount

    if _currentCompiledFunc:
        _currentCompiledFunc._triggerCount += addedTriggerCount
    _currentTriggerCount = currentCounter


def _setCurrentCompiledFunc(func):
    global _currentCompiledFunc

    lastCompiledFunc = _currentCompiledFunc
    _updateFuncTriggerCount()
    _currentCompiledFunc = func
    return lastCompiledFunc


class EUDFuncN:

    def __init__(self, fdecl_func, argn):
        self._argn = argn
        self._fdecl_func = fdecl_func
        functools.update_wrapper(self, fdecl_func)
        self._fstart = None
        self._fend = None
        self._fargs = None
        self._frets = None
        self._triggerCount = None

    def size(self):
        if not self._fstart:
            self._CreateFuncBody()

        return self._triggerCount

    def _CreateFuncBody(self):
        self._triggerCount = 0
        lastCompiledFunc = _setCurrentCompiledFunc(self)

        # Add return point
        self._fend = Forward()

        # Prevent double compilication
        ut.ep_assert(self._fstart is None)

        # Initalize new namespace
        f_bsm = BlockStruManager()
        prev_bsm = SetCurrentBlockStruManager(f_bsm)
        bt.PushTriggerScope()

        f_args = [EUDVariable() for _ in range(self._argn)]
        self._fargs = f_args

        fstart = bt.NextTrigger()
        self._fstart = fstart

        final_rets = self._fdecl_func(*f_args)
        if final_rets is not None:
            self._AddReturn(Assignable2List(final_rets), False)
        fend = bt.RawTrigger()
        bt.PopTriggerScope()

        # Finalize
        ut.ep_assert(f_bsm.empty(), 'Block start/end mismatch inside function')
        SetCurrentBlockStruManager(prev_bsm)

        self._fend << fend

        _setCurrentCompiledFunc(lastCompiledFunc)

    def _AddReturn(self, retv, needjump):
        if self._frets is None:
            self._frets = [EUDVariable() for _ in range(len(retv))]

        ut.ep_assert(
            len(retv) == len(self._frets),
            "Numbers of returned value should be constant."
            " (From function %s)" % self._fdecl_func.__name__
        )

        SetVariables(self._frets, retv)

        if needjump:
            bt.RawTrigger(nextptr=self._fend)

    def __call__(self, *args):
        if self._fstart is None:
            self._CreateFuncBody()

        ut.ep_assert(len(args) == self._argn, 'Argument number mismatch')

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
            SetVariables(tmp_rets, self._frets)
            return List2Assignable(tmp_rets)


def EUDReturn(*args):
    callerName = inspect.stack()[1][3]
    currentFuncName = _currentCompiledFunc.__name__
    if callerName != currentFuncName:
        print('[Warning] EUDReturn may have been called from a '
              'different function (%s) than compiled function(%s)' %
              (callerName, currentFuncName))
    _currentCompiledFunc._AddReturn(args, True)
