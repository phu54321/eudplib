from .stringmap import InitStringMap
from .proptable import InitPropertyMap

_inited = False


def InitMapData(chkt):
    global _inited
    InitStringMap(chkt)
    InitPropertyMap(chkt)
    _inited = True


def IsMapdataInitalized():
    return _inited
