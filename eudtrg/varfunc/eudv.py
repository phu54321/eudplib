from .. import core as c
from .vbase import VariableBase
import weakref
import traceback


class EUDVarBuffer(c.EUDObject):

    """Variable buffer

    40 bytes per variable.
    """

    def __init__(self):
        super().__init__()

        self._varn = 0

    def CreateVarTrigger(self):
        ret = self + (60 * self._varn)
        self._varn += 1
        return ret

    def GetDataSize(self):
        return 2408 + 60 * (self._varn - 1)

    def WritePayload(self, emitbuffer):
        output = bytearray(2408 + 60 * (self._varn - 1))

        for i in range(self._varn):
            # 'preserve trigger'
            output[60 * i + 2376:60 * i + 2380] = b'\x04\0\0\0'

        emitbuffer.WriteBytes(output)


_evb = None


def SetCurrentVariableBuffer(evb):
    global _evb

    oldevb = _evb
    _evb = evb
    return oldevb


class VariableTriggerForward(c.SCMemAddr):

    def __init__(self):
        super().__init__(self)
        self._expr = weakref.WeakKeyDictionary()

    def Evaluate(self):
        if _evb not in self._expr:
            self._expr[_evb] = _evb.CreateVarTrigger()
        return c.Evaluate(self._expr[_evb])


class EUDVariable(VariableBase):

    '''
    Full variable.
    '''

    def __init__(self):
        self._vartrigger = VariableTriggerForward()
        self._varact = self._vartrigger + (8 + 320)

    def GetVTable(self):
        return self._vartrigger

    def GetVariableMemoryAddr(self):
        return self._varact + 20

    # -------

    def QueueAssignTo(self, dest):
        try:
            dest = c.EPD(dest.GetVariableMemoryAddr())
        except AttributeError:
            pass

        return [
            c.SetDeaths(c.EPD(self._varact + 16), c.SetTo, dest, 0),
            c.SetDeaths(c.EPD(self._varact + 24), c.SetTo, 0x072D0000, 0),
        ]

    def QueueAddTo(self, dest):
        try:
            dest = c.EPD(dest.GetVariableMemoryAddr())
        except AttributeError:
            pass

        return [
            c.SetDeaths(c.EPD(self._varact + 16), c.SetTo, dest, 0),
            c.SetDeaths(c.EPD(self._varact + 24), c.SetTo, 0x082D0000, 0),
        ]

    def QueueSubtractTo(self, dest):
        try:
            dest = c.EPD(dest.GetVariableMemoryAddr())
        except AttributeError:
            pass

        return [
            c.SetDeaths(c.EPD(self._varact + 16), c.SetTo, dest, 0),
            c.SetDeaths(c.EPD(self._varact + 24), c.SetTo, 0x092D0000, 0),
        ]

    # -------

    def __add__(self, other):
        t = EUDVariable()
        _Basic_SeqCompute([
            (t, c.SetTo, self),
            (t, c.Add, other)
        ])
        return t

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        t = EUDVariable()
        _Basic_SeqCompute([
            (t, c.SetTo, self),
            (t, c.Subtract, other)
        ])
        return t

    def __rsub__(self, other):
        t = EUDVariable()
        _Basic_SeqCompute([
            (t, c.SetTo, other),
            (t, c.Subtract, self)
        ])
        return t

    def __lshift__(self, other):
        _Basic_SeqCompute((
            (self, c.SetTo, other),
        ))
        return self

    # -------

    def __eq__(self, other):
        if c.IsValidSCMemAddr(other):
            return self.Exactly(other)

        else:
            return (self - other).Exactly(0)

    def __le__(self, other):
        if c.IsValidSCMemAddr(other):
            return self.AtMost(other)

        else:
            t = EUDVariable()
            _Basic_SeqCompute((
                (t, c.SetTo, self),
                (t, c.Subtract, other)
            ))
            return t.Exactly(0)

    def __ge__(self, other):
        if c.IsValidSCMemAddr(other):
            return self.AtLeast(other)

        else:
            t = EUDVariable()
            _Basic_SeqCompute((
                (t, c.SetTo, other),
                (t, c.Subtract, self)
            ))
            return t.Exactly(0)

    def __lt__(self, other):
        if isinstance(other, int) and other <= 0:
            print('[Warning] No unsigned number can be leq than %d' % other)
            traceback.print_stack()
            return [c.Never()]  # No unsigned number is less than 0

        if c.IsValidSCMemAddr(other):
            return self.AtMost(other - 1)

        else:
            t = EUDVariable()
            _Basic_SeqCompute((
                (t, c.SetTo, self),
                (t, c.Add, 1),
                (t, c.Subtract, other)
            ))
            return t.Exactly(0)

    def __gt__(self, other):
        if isinstance(other, int) and other >= 0xFFFFFFFF:
            print('[Warning] No unsigned int can be greater than %d' % other)
            traceback.print_stack()
            return [c.Never()]  # No unsigned number is less than 0

        if c.IsValidSCMemAddr(other):
            return self.AtLeast(other + 1)

        else:
            t = EUDVariable()
            _Basic_SeqCompute((
                (t, c.SetTo, self),
                (t, c.Subtract, 1),
                (t, c.Subtract, other)
            ))
            return t.AtLeast(1)


def _VProc(v, actions):
    nexttrg = c.Forward()

    c.Trigger(
        nextptr=v.GetVTable(),
        actions=[actions] + [c.SetNextPtr(v.GetVTable(), nexttrg)]
    )

    nexttrg << c.NextTrigger()


# From vbuffer.py
def EUDCreateVariables(varn):
    return c.List2Assignable([EUDVariable() for _ in range(varn)])


# _Basic_SeqCompute. Used only in eudv.py
def _Basic_SeqCompute(assignpairs):
    for dst, mdt, src in assignpairs:
        try:
            dstepd = c.EPD(dst.GetVariableMemoryAddr())
        except AttributeError:
            dstepd = dst

        if isinstance(src, EUDVariable):
            if mdt == c.SetTo:
                _VProc(src, [
                    src.QueueAssignTo(dstepd)
                ])

            elif mdt == c.Add:
                _VProc(src, [
                    src.QueueAddTo(dstepd)
                ])

            elif mdt == c.Subtract:
                _VProc(src, [
                    src.QueueSubtractTo(dstepd)
                ])

        else:
            c.Trigger(actions=c.SetDeaths(dstepd, mdt, src, 0))
