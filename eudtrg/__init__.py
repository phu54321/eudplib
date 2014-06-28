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