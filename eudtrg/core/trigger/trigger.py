#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..eudobj import EUDObject
from ..utils import FlattenList
from .triggerscope import NextTrigger, _RegisterTrigger
from .condition import Condition
from .action import Action


_trgcount = 0  # Debugging purpose


def GetTriggerCount():  # Debugging purpose
    return _trgcount


class Trigger(EUDObject):
    def __init__(
            self,
            prevptr=None,
            nextptr=None,
            conditions=None,
            actions=None,
            preserved=True
    ):
        global _trgcount  # Debugging purpose
        _trgcount += 1  # Debugging purpose

        super().__init__()

        _RegisterTrigger(self)  # This should be called before (1)

        if prevptr is None:
            prevptr = 0

        if nextptr is None:
            nextptr = NextTrigger()  # (1)

        if conditions is None:
            conditions = []

        if actions is None:
            actions = []

        conditions = FlattenList(conditions)
        actions = FlattenList(actions)

        assert len(conditions) <= 16, 'Too many conditions'
        assert len(actions) <= 64, 'Too many actions'

        self._prevptr = prevptr
        self._nextptr = nextptr
        self._conditions = conditions
        self._actions = actions
        self._preserved = preserved

        for i, cond in enumerate(self._conditions):
            assert isinstance(cond, Condition)
            cond.SetParentTrigger(self, i)

        for i, act in enumerate(self._actions):
            assert isinstance(act, Action)
            act.SetParentTrigger(self, i)

    def GetDataSize(self):
        return 2408

    def WritePayload(self, pbuffer):
        pbuffer.WriteDword(self._prevptr)
        pbuffer.WriteDword(self._nextptr)

        # Conditions
        for cond in self._conditions:
            cond.WritePayload(pbuffer)

        if len(self._conditions) != 16:
            pbuffer.WriteBytes(bytes(20))
            pbuffer.WriteSpace(20 * (15 - len(self._conditions)))


        # Actions
        for act in self._actions:
            act.WritePayload(pbuffer)

        if len(self._conditions) != 64:
            pbuffer.WriteBytes(bytes(32))
            pbuffer.WriteSpace(32 * (63 - len(self._actions)))

        # Preserved flag

        if self._preserved:
            pbuffer.WriteDword(4)

        else:
            pbuffer.WriteDword(0)

        pbuffer.WriteSpace(28)
