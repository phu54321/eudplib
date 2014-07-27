'''
Basic things
'''

from eudtrglib import LICENSE #@UnusedImport

from .eudfunc import EUDFunc
from .ctrlstru import (
    DoActions,
    EUDJump,
    EUDBranch,
    EUDJumpIf,
    EUDJumpIfNot,
)

from .varassign import SeqCompute, SetVariables
from .vtable import (
    EUDVTable, 
    EUDVariable, 
    EUDLightVariable, 
    VTProc
)

from .vbuffer import EUDCreateVariables
