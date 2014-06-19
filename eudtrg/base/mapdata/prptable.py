from .unitprp import UnitProperty
from .mapdata import uprptable, uprpdict

def ParseProperty(prop):
    assert isinstance(prop, UnitProperty), 'Unknown type %s given. (UPRP in map template is ignored)' % type(prop)
    
    prop = bytes(prop)
    try:
        return uprpdict[prop]
    
    except KeyError:
        uprpindex = len(uprptable)
        assert uprpindex < 64, 'Unit property table overflow'
        
        uprptable.append(prop)
        return uprpindex