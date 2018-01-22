from .. import (
    core as c,
    utils as ut
)

import functools
import rand


mdbg_dbepd = c.EPD(c.Db(b'EUDPLIBTRACETOOL' + bytes(4 * 2048)))
recordTraceAct = c.Forward()
c.PushTriggerScope()
recordTraceTrigger = c.RawTrigger(
    actions=[
        recordTraceAct << c.SetMemoryEPD(mdbg_dbepd + 4, c.SetTo, 0)
    ]
)
c.PopTriggerScope()


def EUDTraced(f):
    """Push trace stack for that function.

    Arguments:
        f {EUDFunc} -- Any function that wants to have their trace stack
    """
    @functools.wraps(f)
    def _(*args, **kwargs):
        c.RawTrigger(c.SetMemory(recordTraceAct + 16, c.Add, 1))
        rets = f(*args, **kwargs)
        EUDLogTrace(0)
        c.RawTrigger(c.SetMemory(recordTraceAct + 16, c.Subtract, 1))
        return rets
    return _


nextTraceId = 0
traceMap = []
traceKey = 0


def resetTrace():
    global nextTraceId
    nextTraceId = 0
    traceMap.clear()


c.RegisterCreatePayloadCallback(resetTrace)


def EUDLogTrace(msg):
    """Log trace.

    Arguments:
        msg {str} -- Any message that you want to associate with the message.
    """
    global nextTraceId
    v = nextTraceId
    nextTraceId += 1
    traceMap.append(msg)

    nt = c.Forward()
    c.RawTrigger(
        nextptr=recordTraceTrigger,
        actions=[
            c.SetNextPtr(recordTraceTrigger, nt),
            c.SetMemory(recordTraceAct + 20, c.SetTo, v)
        ]
    )
    nt << c.NextTrigger()


def EUDGetTraceMap():
    return traceMap
