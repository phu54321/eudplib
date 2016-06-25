import weakref
import collections

from .. import rawtrigger as bt
from ..allocator import (
    Evaluate,
    Forward,
    ConstExpr,
    IsValidExpr,
    ExprProxy
)

from ...utils import (
    EPD,
    ep_assert
)

from .eudv import EUDVariable, SeqCompute
from .vbuf import GetCurrentVariableBuffer


class EUDVArrayData(ConstExpr):
    def __init__(self, initvars):
        super().__init__(self)
        self._initvars = initvars
        self._vdict = weakref.WeakKeyDictionary()

    def Evaluate(self):
        evb = GetCurrentVariableBuffer()
        if evb not in self._vdict:
            variables = [evb.CreateVarTrigger(ival) for ival in self._initvars]
            self._vdict[evb] = variables[0]

        return Evaluate(self._vdict[evb])


class EUDVArray(ExprProxy):
    def __init__(self, initvars):
        if isinstance(initvars, int):
            initvars = [0] * initvars

        if isinstance(initvars, collections.Iterable):
            baseobj = EUDVArrayData(initvars)

        elif IsValidExpr(initvars):
            baseobj = initvars
        else:
            baseobj = EUDVariable()
            baseobj << initvars

        super().__init__(baseobj)
        self._epd = EPD(self)

    def getItemPtr(self, i):
        return self + 60 * i

    def getItemEPD(self, i):
        return self._epd + 15 * i

    def get(self, i):
        # This function is hand-optimized

        ret = EUDVariable()
        itemptr = self.getItemPtr(i)
        itemepd = self.getItemEPD(i)

        vtproc = Forward()
        nptr = Forward()
        a0, a1, a2 = Forward(), Forward(), Forward()

        SeqCompute([
            (EPD(vtproc + 4), bt.SetTo, itemptr),
            (EPD(a0 + 16), bt.SetTo, itemepd + (8 + 320 + 16) // 4),
            (EPD(a1 + 16), bt.SetTo, itemepd + (8 + 320 + 24) // 4),
            (EPD(a2 + 16), bt.SetTo, itemepd + 1),
        ])

        vtproc << bt.RawTrigger(
            nextptr=0,
            actions=[
                a0 << bt.SetDeaths(0, bt.SetTo, EPD(ret.getValueAddr()), 0),
                a1 << bt.SetDeaths(0, bt.SetTo, 0x072D0000, 0),
                a2 << bt.SetDeaths(0, bt.SetTo, nptr, 0),
            ]
        )

        nptr << bt.NextTrigger()
        return ret

    def set(self, i, value):
        itemepd = self.getItemEPD(i)
        a0, t = Forward(), Forward()
        SeqCompute([
            (EPD(a0 + 16), bt.SetTo, itemepd + (8 + 320 + 20) // 4),
            (EPD(a0 + 20), bt.SetTo, value),
        ])
        t << bt.RawTrigger(
            actions=[
                a0 << bt.SetDeaths(0, bt.SetTo, 0, 0),
            ]
        )

    def __getitem__(self, i):
        return self.get(i)

    def __setitem__(self, i, value):
        return self.set(i, value)
