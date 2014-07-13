from eudtrg import LICENSE #@UnusedImport

from .eudfunc import EUDFunc, Make_EUDFunc
from .vtable import EUDVTable, EUDVariable,EUDCreateVariables, VTProc
from .ctrlstru import (
    DoActions,
    EUDJump,
    EUDBranch,
    EUDJumpIf,
    EUDJumpIfNot,
    EUDWhile
)

from .varassign import SetVariables, SeqCompute, DerefWrite

from .readdword import f_dwread
from .arithmetic import f_add, f_sub, f_mul, f_div
from .dwordbreak import f_dwbreak
from .epdcalc import f_epd

from .pselect import InitPlayerSwitch
