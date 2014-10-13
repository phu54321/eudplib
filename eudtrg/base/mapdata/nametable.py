'''
Parses strings that could refer to template maps.
'''

'''
Copyright (c) 2014 trgk

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
   3. This notice may not be removed or altered from any source
   distribution.
'''

from ..trgstrconst import UnitNameDict
from ..utils import ubconv
from .mapdata import strtable, unitnametable, locnametable


# Data getter
def ParseLocation(locname):
    '''
    :param locname: Location name
    :returns: Corresponding location name.
    :raises RuntimeError: Location name is ambigious or not defined.
    '''
    try:
        string = ubconv.u2b(locname)

        # try map-defined location name
        try:
            locidx = locnametable[string]
            if not locidx:
                raise RuntimeError(
                    'Ambigious location name %s used in template map'
                    % locname)
            return locidx

        except KeyError:
            pass

        raise RuntimeError('Unknown location name %s' % locname)

    except TypeError:
        return locname


def ParseUnit(unitname):
    '''
    :param unitname: Unit name, with or without color characters.
    :returns: Corresponding Unit ID.
    :raises RuntimeError:
        1. Unit name may match multiple units.
        2. There is no corresponding unit to given unit name.
    '''
    try:
        # try map-defined unit name
        try:
            string = ubconv.u2b(unitname)
            unitidx = unitnametable[string]
            if not unitidx:
                raise RuntimeError(
                    'Ambigious unit name %s used in template map' % unitname)
            return unitidx

        except KeyError:
            pass

        # try default unit name
        try:
            string = unitname
            unitidx = UnitNameDict[string]
            return unitidx

        except KeyError:
            pass

        raise RuntimeError('Unknown unit name %s' % unitname)

    except TypeError:
        return unitname  # maybe int


def ParseString(string):
    '''
    :param string: String
    :returns: Corresponding string number. This function creates new string
        if there isn't existing one. String with same contents will have same
        string ID.

    :raises AssertionError: String table exceeded 65536 bytes.
    '''
    try:
        bstring = ubconv.u2b(string)
        return strtable.GetStringIndex(bstring)

    except TypeError:
        return string
