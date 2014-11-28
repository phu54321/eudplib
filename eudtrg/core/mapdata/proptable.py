'''
Unit property table manager.
'''

from .unitprp import UnitProperty

_uprpdict = {}
_uprptable = []


def InitPropertyMap(chkt):
    global _prptable, _uprpdict
    _uprpdict.clear()
    _uprptable.clear()


def GetPropertyIndex(prop):
    assert isinstance(prop, UnitProperty)

    prop = bytes(prop)
    try:
        return _uprpdict[prop] + 1  # SC counts unit properties from 1. Sucks

    except KeyError:
        uprpindex = len(_uprptable)
        assert uprpindex < 64, 'Unit property table overflow'

        _uprptable.append(prop)
        _uprpdict[prop] = uprpindex
        return uprpindex + 1  # SC counts unit properties from 1. Sucks


def ApplyPropertyMap(chkt):
    uprpdata = b''.join(_uprptable) + bytes(20 * (64 - len(_uprptable)))
    chkt.setsection('UPRP', uprpdata)
