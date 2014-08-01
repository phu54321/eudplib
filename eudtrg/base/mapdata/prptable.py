'''
Unit property table manager.
'''

from eudtrg import LICENSE  # @UnusedImport

from .unitprp import UnitProperty
from .mapdata import uprptable, uprpdict


def ParseProperty(prop):
    '''
    :param prop: Unit property
    :type prop: :class:`UnitProperty`
    :returns: Corresponding property ID. Identical Properties will have same
        property ID.

    :raises AssertionError: More than 64 different properties have been used.
    '''
    assert isinstance(prop, UnitProperty), (
        'UnitProperty type needed, but %s given.' % type(prop))

    # convert to bytes.
    prop = bytes(prop)
    try:
        return uprpdict[prop] + 1  # SC counts unit properties from 1. Sucks

    except KeyError:
        uprpindex = len(uprptable)
        assert uprpindex < 64, 'Unit property table overflow'

        uprptable.append(prop)
        uprpdict[prop] = uprpindex
        return uprpindex + 1  # SC counts unit properties from 1. Sucks
