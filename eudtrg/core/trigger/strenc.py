from ..mapdata import (
    GetLocationIndex,
    GetStringIndex,
    GetSwitchIndex,
    GetUnitIndex,
    IsMapdataInitalized
)

from ..utils import u2b, b2i4

from .strdict import (
    DefAIScriptDict,
    DefLocationDict,
    DefSwitchDict,
    DefUnitDict
)


def EncodeAIScript(ais):
    if type(ais) is str:
        ais = u2b(ais)

    if type(ais) is bytes:
        assert len(ais) >= 4, 'AIScript name too short'

        if len(ais) > 4:
            return b2i4(DefAIScriptDict[ais])

        elif len(ais) == 4:
            return b2i4(ais)

    else:
        return ais


def _EncodeAny(f, dl, s):
    try:
        return f(s)

    except:
        try:
            return dl.get(s, s)

        except TypeError:  # unhashable
            return s


def EncodeLocation(loc):
    return _EncodeAny(lambda s: GetLocationIndex(s) + 1, DefLocationDict, loc)


def EncodeString(s):
    return _EncodeAny(GetStringIndex, {}, s)


def EncodeSwitch(sw):
    return _EncodeAny(GetSwitchIndex, DefSwitchDict, sw)


def EncodeUnit(u):
    return _EncodeAny(GetUnitIndex, DefUnitDict, u)
