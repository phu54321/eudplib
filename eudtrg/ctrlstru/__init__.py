#!/usr/bin/python
#-*- coding: utf-8 -*-

from .basicstru import (
    DoActions,
    EUDJump,
    EUDBranch,
    EUDJumpIf,
    EUDJumpIfNot,
)

from .simpleblock import (
    EUDIf,
    EUDIfNot,
    EUDElseIf,
    EUDElseIfNot,
    EUDElse,
    EUDEndIf,

    EUDExecuteOnce,
    EUDEndExecuteOnce,
)

from .loopblock import(
    EUDInfLoop,
    EUDEndInfLoop,

    EUDWhile,
    EUDWhileNot,
    EUDEndWhile,

    EUDLoopContinue,
    EUDLoopContinueIf,
    EUDLoopContinueIfNot,
    EUDLoopSetContinuePoint,
    EUDLoopBreak,
    EUDLoopBreakIf,
    EUDLoopBreakIfNot,
)

from .swblock import (
    EUDSwitch,
    EUDSwitchCase,
    EUDSwitchDefault,
    EUDSwitchBreak,
    EUDEndSwitch,
)

from .breakcont import (
    EUDContinue,
    EUDContinueIf,
    EUDContinueIfNot,
    EUDSetContinuePoint,

    EUDBreak,
    EUDBreakIf,
    EUDBreakIfNot
)
