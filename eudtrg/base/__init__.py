'''
Core of eudtrg. Everything in eudtrg are implemented using eudtrg.base
Core defines

- EUD Object (EUDObject class)
- Trigger (Trigger, Condition, Action class)
- Raw bytes object (Db)
- Calculation of expression containing addresses. (Expr class)
- Map reading/writing (LoadMap, SaveMap)

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

from .stocktrg import *
from .trgconst import *
from .utils.utils import *
from .utils.ubconv import UbconvUseCharset
