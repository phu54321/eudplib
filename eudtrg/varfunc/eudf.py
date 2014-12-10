#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import inspect

from .. import core as c
from ..core.utils.blockstru import (
    BlockStruManager,
    SetCurrentBlockStruManager
)
from .eudv import EUDVariable, SeqCompute


class EUDFunc:
    def __init__(self, fdecl_func):
        # Get argument number of fdecl_func
        argspec = inspect.getargspec(fdecl_func)
        assert argspec[1] is None, (
            'No variadic arguments (*args) allowed for EUDFunc.')
        assert argspec[2] is None, (
            'No variadic keyword arguments (*kwargs) allowed for EUDFunc.')

        self._argn = len(argspec[0])
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

        if c.PushTriggerScope():
            f_args = [EUDVariable() for _ in range(self._argn)]
            fstart = c.NextTrigger()
            f_rets = self._fdecl_func(*f_args)
            if f_rets is not None:
                f_rets = c.Assignable2List(f_rets)
            fend = c.Trigger()
        c.PopTriggerScope()

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
            [(farg, c.SetTo, arg) for farg, arg in zip(self._fargs, args)]
        )

        # Call body
        fcallend = c.Forward()

        c.Trigger(
            nextptr=self._fstart,
            actions=[c.SetNextPtr(self._fend, fcallend)]
        )

        fcallend << c.NextTrigger()

        if self._frets is not None:
            retn = len(self._frets)
            tmp_rets = [EUDVariable() for _ in range(retn)]
            SeqCompute(
                [(tr, c.SetTo, r) for tr, r in zip(tmp_rets, self._frets)]
            )
            return c.List2Assignable(tmp_rets)


def SetVariables(srclist, dstlist, mdtlist=None):
    srclist = c.FlattenList(srclist)
    dstlist = c.FlattenList(dstlist)
    assert len(srclist) == len(dstlist), 'Input/output size mismatch'

    if mdtlist is None:
        mdtlist = [c.SetTo] * len(srclist)

    sqa = [(src, mdt, dst) for src, dst, mdt in zip(srclist, dstlist, mdtlist)]
    SeqCompute(sqa)
