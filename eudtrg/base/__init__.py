'''
Core of eudtrg. Everything in eudtrg are implemented using eudtrg.base
Core defines

- EUD Object (EUDObject class)
- Trigger (Trigger, Condition, Action class)
- Raw bytes object (Db)
- Calculation of expression containing addresses. (Expr class)
- Map reading/writing (LoadMap, SaveMap)

'''

 

from .dataspec.eudobj import EUDObject  # noqa
from .dataspec.forward import Forward
from .dataspec.trigger import (
    PushTriggerScope,
    PopTriggerScope,
    Trigger,
    Condition,
    Action,
    NextTrigger,
    Disabled,
    triggerend
)

from .dataspec.expr import Expr
from .dataspec.bytedump import Db
from .dataspec.struoffset import CreateOffsetMapping

from .mapdata.maprw import LoadMap, SaveMap
from .mapdata.unitprp import UnitProperty
from .mapdata.doevents import EUDDoEvents

from .stocktrg import *
from .trgconst import *
from .utils.utils import *
from .utils.ubconv import UbconvUseCharset
