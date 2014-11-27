from .stringmap import InitStringMap
from .proptable import InitPropertyMap

_inited = False
_chkt = None
_rawfile = None


def InitMapData(chkt, rawfile):
    global _inited, _chkt, _rawfile
    _chkt = chkt
    _rawfile = rawfile

    InitStringMap(chkt)
    InitPropertyMap(chkt)
    _inited = True


def IsMapdataInitalized():
    return _inited


def GetChkTokenized():
    return _chkt
