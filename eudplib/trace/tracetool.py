from .. import (
    core as c,
    utils as ut
)

import os
from . import tracecrypt


traceToolDataEPD = ut.EPD(c.Db(b'EUDPLIBTRACETOOL' + bytes(4 * 2048)))
recordTraceAct = c.Forward()
c.PushTriggerScope()
recordTraceTrigger = c.RawTrigger(
    actions=[
        recordTraceAct << c.SetMemoryEPD(traceToolDataEPD + 4, c.SetTo, 0)
    ]
)
c.PopTriggerScope()


def EUDTracePush():
    c.RawTrigger(actions=c.SetMemory(recordTraceAct + 16, c.Add, 1))


def EUDTracePop():
    EUDTraceLogRaw(0)
    c.RawTrigger(actions=c.SetMemory(recordTraceAct + 16, c.Subtract, 1))


nextTraceId = 0
traceMap = []
traceKey = 0


def _ResetTraceMap():
    """This function gets called by savemap.py::SaveMap to clear trace data."""
    global nextTraceId
    global traceKey
    nextTraceId = 0
    traceKey = ut.b2i4(os.urandom(4))
    traceMap.clear()


def EUDTraceLog(msg):
    """Log trace.

    Arguments:
        msg {str} -- Any message that you want to associate with the message.
    """

    global nextTraceId
    v = nextTraceId
    v2 = tracecrypt.mix(v, traceKey)
    nextTraceId += 1
    traceMap.append((v2, str(msg)))

    EUDTraceLogRaw(v2)


def EUDTraceLogRaw(v2):
    nt = c.Forward()
    c.RawTrigger(
        nextptr=recordTraceTrigger,
        actions=[
            c.SetNextPtr(recordTraceTrigger, nt),
            c.SetMemory(recordTraceAct + 20, c.SetTo, v2)
        ]
    )
    nt << c.NextTrigger()


def _GetTraceMap():
    return traceMap
