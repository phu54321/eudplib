'''
Variable buffer.
'''

from eudtrg import LICENSE #@UnusedImport
from eudtrg.base import * #@UnusedWildImport
from .vtable import *

'''
# Variable recycling thing. Not yet tested

_lastvtvars = EUDVTable(32).GetVariables()
_lastvt_filled = 32

# Variable tank
def EUDCreateVariables(varn):
    
    global _lastvt_filled
    global _lastvtvars

    variables = []

    while varn:
        vt_popnum = min(32 - _lastvt_filled, varn)
        variables.extend(_lastvtvars[_lastvt_filled : _lastvt_filled + vt_popnum])
        _lastvt_filled += vt_popnum
        varn -= vt_popnum

        if _lastvt_filled == 32:
            vt = EUDVTable(32)
            _lastvtvars = vt.GetVariables()
            _lastvt_filled = 0

    return List2Assignable(variables)
'''

def EUDCreateVariables(varn):
    return EUDVTable(varn).GetVariables()