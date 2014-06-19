from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVTable
from .eudfunc import EUDFunc

f_dwread = None

def _ReadDwordInit():
    global f_dwread

    vt = EUDVTable(2)
    targetplayer, ret = vt.GetVariables()

    readstart = Forward()
    readend = Forward()

    f_dwread = EUDFunc(readstart, readend, vt, 1, 1)


    """
    Pseudocode
        ret = 0xFFFFFFFF

        static_for(i = 31, 30, ... , 0) {
            ret -= 2**i
            ifnot ret(cmptrigger_number) >= target(cmptrigger_player): // chain[i]
                continue

            ret += 2**i
        }
    """


    # Common comparison trigger
    cmp = Forward()
    cmp_player = cmp + 4
    cmp_number = cmp + 8
    cmpact = Forward()

    cmptrigger = Forward()
    cmptrigger << Trigger(
        conditions = [
            cmp << Memory(0, AtMost, 0)
        ],
        actions = [
            cmpact << SetMemory(cmptrigger + 4, SetTo, 0)
        ]
    )
    cmpact_ontrueaddr = cmpact + 20

    # static_for
    chain1 = [Forward() for _ in range(32)]
    chain2 = [Forward() for _ in range(32)]


    # Main logic start
    readstart << Trigger(
        nextptr = vt,
        actions = [
            targetplayer.QueueAssignTo(EPD(cmp_player)),

            # num = 0xFFFFFFFF
            SetMemory(cmp_number, SetTo, 0xFFFFFFFF),
            ret.SetNumber(0xFFFFFFFF),

            SetNextPtr(vt, chain1[31])
        ]
    )

    for i in range(31, -1, -1):
        nextchain = chain1[i-1] if i > 0 else readend

        chain1[i] << Trigger(
            nextptr = cmptrigger,
            actions = [
                SetMemory(cmp_number, Subtract, 2**i),
                ret.SubtractNumber(2**i),
                SetNextPtr(cmptrigger, chain2[i]),
                SetMemory(cmpact_ontrueaddr, SetTo, nextchain)
            ]
        )

        chain2[i] << Trigger(
            actions = [
                SetMemory(cmp_number, Add, 2**i),
                ret.AddNumber(2**i)
            ]
        )

    readend << Trigger()

_ReadDwordInit()
