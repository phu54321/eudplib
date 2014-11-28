from .stringmap import InitStringMap, ApplyStringMap
from .proptable import InitPropertyMap, ApplyPropertyMap

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


def UpdateMapData():
    ApplyStringMap(_chkt)
    ApplyPropertyMap(_chkt)


def IsMapdataInitalized():
    return _inited


def GetChkTokenized():
    return _chkt


def GetRawFile():
    return _rawfile
