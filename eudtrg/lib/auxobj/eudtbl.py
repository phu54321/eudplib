from eudtrg import *
from eudtrg.base.utils.sctbl import TBL
from eudtrg.base.utils.ubconv import u2b
from eudtrg.lib.baselib import *
from ..auxfunc.readdword import f_dwread

class EUDTbl(EUDObject):
    def __init__(self):
        super().__init__()

        # convert & store
        self._tbl = TBL()

    def StringIndex(self, string):
        bstring = u2b(string)
        return self._tbl.GetStringIndex(bstring)

    def SetAsDefault(self):
        DoActions(SetMemory(0x5993D4, SetTo, self))



    def SetAddress(self, addr):
        super().SetAddress(addr)
        self._tbldata = self._tbl.SaveTBL()

    def ResetAddress(self):
        super().ResetAddress()
        self._tbldata = None


    def GetDataSize(self):
        return len(self._tbldata)

    def GetDependencyList(self):
        return []

    def WritePayload(self, buf):
        buf.EmitBytes(self._tbldata)



_origtbladdr = EUDCreateVariables(1)

def f_initeudtbl():
    SetVariables(_origtbladdr, f_dwread(EPD(0x5993D4)))

def f_reseteudtbl():
    SeqCompute([ (EPD(0x5993D4), SetTo, _origtbladdr) ])