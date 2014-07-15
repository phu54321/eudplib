'''
Core of eudtrg. Everything in eudtrg are implemented using eudtrg.base
Core defines
 - EUD Object (EUDObject class)
 - Trigger (Trigger, Condition, Action class)
 - Raw bytes object (Db)
 - Calculation of expression containing addresses. (Expr class)
 - Map reading/writing (LoadMap, SaveMap)
'''

from eudtrg import LICENSE #@UnusedImport

from .dataspec.eudobj import EUDObject
from .dataspec.forward import Forward
from .dataspec.trigger import (
    GetTriggerCount,
    PushTriggerScope,
    PopTriggerScope,
    Trigger,
    Condition,
    Action,
    NextTrigger,
    Disabled,
    triggerend
)

from .dataspec.bytedump import Db

from .mapdata.maprw import LoadMap, SaveMap
from .mapdata.unitprp import UnitProperty

from .stocktrg import *
from .trgconst import *

from .utils.utils import *
from .utils.ubconv import UbconvUseCharset
