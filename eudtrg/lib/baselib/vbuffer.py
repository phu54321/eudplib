'''
Variable buffer.
'''

from eudtrg import LICENSE #@UnusedImport
from eudtrg.base import * #@UnusedWildImport
from .vtable import *



_lastvtvars = EUDVTable(32).GetVariables()
_lastvt_filled = 32

def EUDCreateVariables(varn):
    '''
    Create (varn) :class:`EUDVariables`. Returned variables are not guarranted 
    to be in the same variable table.

    :param varn: Number of EUDVariables to create.
    :returns: List of variables. If varn is 1, then a variable is returned.
    '''
    
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
