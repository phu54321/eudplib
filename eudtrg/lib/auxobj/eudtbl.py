from eudtrg import *
from eudtrg.base.utils.sctbl import TBL
from eudtrg.base.utils.ubconv import u2b
from eudtrg.lib.baselib import *
from ..auxfunc.readdword import f_dwread_epd


class EUDTbl(EUDObject):

    '''
    Custom string table.
    '''

    def __init__(self):
        super().__init__()

        # convert & store
        self._tbl = TBL()

    def StringIndex(self, string):
        '''
        Get string index of certain string inside string table.
        :param string: String to get index.
        :returns: String index.
        :raises AssertionError: String table exceeds 65536 bytes.
        '''
        bstring = u2b(string)
        return self._tbl.GetStringIndex(bstring)

    def SetAsDefault(self):
        '''
        Set default string table to self. All strings used by DisplayText will
        be forwarded to current string table

        .. warning::
            Always call :func:`f_initeudtbl` before using this function.
            Always call :func:`f_reseteudtbl` after using this function.
        '''
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
    '''
    Backup original string table address.
    '''
    SetVariables(_origtbladdr, f_dwread_epd(EPD(0x5993D4)))


def f_reseteudtbl():
    '''
    Restore string table address. If you used custom string table, then you
    should call this function before trigger loop ends.
    '''
    SeqCompute([(EPD(0x5993D4), SetTo, _origtbladdr)])
