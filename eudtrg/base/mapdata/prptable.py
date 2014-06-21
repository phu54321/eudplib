'''
Unit property table manager.
'''

from eudtrg import LICENSE #@UnusedImport

from .unitprp import UnitProperty
from .mapdata import uprptable, uprpdict

def ParseProperty(prop):
    '''
    UnitProperty -> property id.
    '''
    assert isinstance(prop, UnitProperty), 'UnitProperty type needed, but %s given.' % type(prop)
    
    # convert to bytes.
    prop = bytes(prop)
    try:
        return uprpdict[prop] + 1 # SC counts unit properties from 1. Sucks
    
    except KeyError:
        uprpindex = len(uprptable)
        assert uprpindex < 64, 'Unit property table overflow'
        
        uprptable.append(prop)
        uprpdict[prop] = uprpindex
        return uprpindex + 1 # SC counts unit properties from 1. Sucks