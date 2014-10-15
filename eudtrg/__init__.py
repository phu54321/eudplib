 #!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 trgk

# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#    3. This notice may not be removed or altered from any source
#    distribution.
#
# See eudtrg.LICENSE for more info


'''
eudtrg library. This library follows zlib license.
eudtrg consists of 2 subpackages.

- base : Core of eudtrg. lib is implemented using base subpackage.
- lib  : Libraries made using 'base'.
'''

from .base import *
from .lib import *

__version__ = "0.30-r2-beta"


def eudtrgVersion():
    return __version__

'''
Changelog

0.30-r1
 - SaveMap syntax changed.

0.23-r2
 - eudtrg now alerts about payload size.

0.23-r1
 - Added some intro messages for non-euda-enabled players.
 - New easier EUDFunc syntax. Now you can just convert normal python function
  to EUD function by only decorating it with EUDFunc


    @EUDFunc
    def f_add(a, b):
        ret = EUDCreateVariables(1)
        SeqCompute([
            (ret, SetTo, 0),
            (ret, Add, a),
            (ret, Add, b)
        ])

        return ret


 - Added EUDLightVariable.


0.22-r1
 - eudtrg now requires only 1 computer player to work properly.
 - Added EUDCreateVariables in baselib.vtable. Instead of writing

    vt = EUDVTable(3)
    a, b, c = vt.GetVariables()
  
  you can just write

    a, b, c = EUDCreateVariables(3)

'''
