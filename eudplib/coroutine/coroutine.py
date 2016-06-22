from .. import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)

from ..trigger import Trigger


firstCoroutine = c.EUDVariable()
lastCoroutine = c.EUDVariable()


class Coroutine:
    def __init__(self, func):
        # Convert target to eudfunc
        if not isinstance(func, c.EUDFunc):
            func = c.EUDFunc(func)

        ut.ep_assert(
            func._argn == 0 and func._retn == 0,
            "Only function with no argument/returns is allowed."
        )

        self._targetfunc = func
        self._running = c.EUDLightVariable()

        self._endp = c.RawTrigger()
        self._resumep = c.EUDVariable(func._fstart)

    def run(self):
        if cs.EUDIf(self._running.Exactly(0)):
            self.
            pass
        cs.EUDEndIf()

