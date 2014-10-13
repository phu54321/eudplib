'''
Variable buffer.
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
from eudtrg.base import *  # @UnusedWildImport


from . import vtable


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
        variables.extend(
            _lastvtvars[_lastvt_filled: _lastvt_filled + vt_popnum]
            )
        _lastvt_filled += vt_popnum
        varn -= vt_popnum

        if _lastvt_filled == 32:
            vt = vtable.EUDVTable(32)
            _lastvtvars = vt.GetVariables()
            _lastvt_filled = 0

    return List2Assignable(variables)
