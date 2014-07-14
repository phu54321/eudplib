'''
Basic things
'''

from eudtrg import LICENSE #@UnusedImport

from .eudfunc import EUDFunc
from .ctrlstru import (
    DoActions,
    EUDJump,
    EUDBranch,
    EUDJumpIf,
    EUDJumpIfNot,
    EUDWhile
)

from .varassign import SeqCompute, SetVariables
from .vtable import EUDVTable, EUDVariable, EUDCreateVariables
