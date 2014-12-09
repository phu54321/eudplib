from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf
from ..memiof import f_dwread_epd, f_dwwrite_epd


class ExtendedString(c.EUDObject):
    def __init__(self, content):
        super().__init__()
        self.content = c.u2b(content)

    def GetDataSize(self):
        return len(self.content) + 5

    def WritePayload(self, pbuf):
        pbuf.WriteBytes(b'\x01\x00\x04\x00')
        pbuf.WriteBytes(self.content)
        pbuf.WriteByte(0)

    def GetDisplayAction(self):
        resetter = c.Forward()
        fw = c.Forward()
        acts = [
            c.SetMemory(0x5993D4, c.SetTo, self),
            c.DisplayText(fw),
            resetter << c.SetMemory(0x5993D4, c.SetTo, 0)
        ]
        fw << ExtendedStringIndex_FW(resetter)
        return acts


class ExtendedStringIndex_FW(c.SCMemAddr):
    def __init__(self, resetter):
        super().__init__(self)
        self._resetter = resetter

    def Evaluate(self):
        _RegisterResetterAction(self._resetter)
        return c.RlocInt(1, 0)


_resetteracts = set()


def RCPC_ResetActionSet():
    _resetteracts.clear()


c.RegisterCreatePayloadCallback(RCPC_ResetActionSet)


def _RegisterResetterAction(resetteract):
    _resetteracts.add(resetteract)


class ResetterBuffer(c.EUDObject):
    def __init__(self):
        super().__init__()

    def GetDataSize(self):
        return (len(_resetteracts) + 1) * 4

    def WritePayload(self, pbuf):
        for ra in _resetteracts:
            pbuf.WriteDword(c.EPD(ra + 20))
        pbuf.WriteDword(0xFFFFFFFF)


_extstr_dict = {}


def DisplayExtText(text):
    text = c.u2b(text)
    if text not in _extstr_dict:
        _extstr_dict[text] = ExtendedString(text)
    return _extstr_dict[text].GetDisplayAction()


def f_initextstr():
    rb = ResetterBuffer()
    ptr, v = vf.EUDVariable(), vf.EUDVariable()
    ptr << c.EPD(rb)
    origstrptr = f_dwread_epd(c.EPD(0x5993D4))

    vf.SeqCompute((
        (1, c.SetTo, origstrptr),
        (2, c.SetTo, origstrptr.GetVariableMemoryAddr()),
        (3, c.SetTo, ptr)
    ))

    if cs.EUDInfLoop():
        v << f_dwread_epd(ptr)
        cs.EUDBreakIf(v == 0xFFFFFFFF)
        f_dwwrite_epd(v, origstrptr)
        ptr += 1

    cs.EUDEndInfLoop()
