'''
eudtrg library. This library follows zlib license.
eudtrg consists of 3 subpackages.
 base : Core of eudtrg. baselib and auxlib is implemented with base subpackage.
 baselib : Basic library. Memory rw, Multiply/Division, etc
 auxlib : Some more high-level libraries such as GRP.
'''

from eudtrg import LICENSE #@UnusedImport

from .base import *
from .baselib import *

__version__ = "0.22-r2"

def eudtrgVersion():
    return __version__

'''
Changelog

0.22-r2
 - Added some intro messages for non-euda-enabled players.
 - New easier eudfunc syntax

 

0.22-r1
 - eudtrg now requires only 1 computer player to work properly.
 - Added EUDCreateVariables in baselib.vtable. Instead of writing

    vt = EUDVTable(3)
    a, b, c = vt.GetVariables()
  
  you can just write

    a, b, c = EUDCreateVariables(3)

'''