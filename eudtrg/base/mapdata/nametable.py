from eudtrg import LICENSE #@UnusedImport

from ..trgstrconst import UnitNameDict
from ..utils import ubconv
from .mapdata import strtable, unitnametable, locnametable


# Data getter
def ParseLocation(locstring):
    try:
        string = ubconv.u2b(locstring)

        # try map-defined location name
        try:
            locidx = locnametable[string]
            if not locidx:
                raise RuntimeError('Duplicated location name %s used in template map' % locstring)
            return locidx

        except KeyError:
            pass

        raise RuntimeError('Unknown location name %s' % locstring)

    except TypeError:
        return locstring


def ParseUnit(unitstring):
    try:
        # try map-defined location name
        try:
            string = ubconv.u2b(unitstring)
            unitidx = unitnametable[string]
            if not unitidx:
                raise RuntimeError('Duplicated unit name %s used in template map' % unitstring)
            return unitidx

        except KeyError:
            pass

        # try default unit name
        try:
            string = unitstring
            unitidx = UnitNameDict[string]
            return unitidx

        except KeyError:
            pass

        raise RuntimeError('Unknown unit name %s' % unitstring)

    except TypeError:
        return unitstring # maybe int



def ParseString(string):
    try:
        bstring = ubconv.u2b(string)
        return strtable.GetStringIndex(bstring)
    
    except TypeError:
        return string


