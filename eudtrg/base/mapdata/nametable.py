'''
Parses strings that could refer to template maps.
'''

from eudtrg import LICENSE #@UnusedImport

from ..trgstrconst import UnitNameDict
from ..utils import ubconv
from .mapdata import strtable, unitnametable, locnametable


# Data getter
def ParseLocation(locstring):
    '''
    Location name -> Location id.
     - type(locstring) is int : return as-is
     - type(locstring) in [str, bytes]: find it in template map.
       If matching location name -> return its location id
       If location name is ambigious -> raise RuntimeError
       If location name not found -> raise Runtimeerror
    '''
    try:
        string = ubconv.u2b(locstring)

        # try map-defined location name
        try:
            locidx = locnametable[string]
            if not locidx:
                raise RuntimeError('Ambigious location name %s used in template map' % locstring)
            return locidx

        except KeyError:
            pass

        raise RuntimeError('Unknown location name %s' % locstring)

    except TypeError:
        return locstring


def ParseUnit(unitstring):
    '''
    Unit name -> Unit ID.
     - type(unitstring) is int : return as-is
     - type(unitstring) in [str, bytes]: find it in template map / default names.
       If matching unit name in template map -> return is unit id
       If matching unit name in stock unit name -> return its unit id
       If unit name is ambigious -> raise RuntimeError
       If unit name not found -> raise RuntimeError.
    '''
    try:
        # try map-defined location name
        try:
            string = ubconv.u2b(unitstring)
            unitidx = unitnametable[string]
            if not unitidx:
                raise RuntimeError('Ambigious unit name %s used in template map' % unitstring)
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
    '''
    String -> string id.
     - type(string) is int : return as-is.
     - type(string) in [str, bytes]:
       If matching string -> returns its string id.
       If no match -> Creates new string & returns its id.
        (May cause string overflow error.)
    '''
    try:
        bstring = ubconv.u2b(string)
        return strtable.GetStringIndex(bstring)
    
    except TypeError:
        return string


