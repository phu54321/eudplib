'''
eudtrg library. This library follows zlib license.
eudtrg consists of 2 subpackages.

- base : Core of eudtrg. lib is implemented using base subpackage.
- lib  : Libraries made using 'base'.
'''

from eudtrg import LICENSE #@UnusedImport

from .base import *
from .lib import *

__version__ = "0.30-r1-beta"

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