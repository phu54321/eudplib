from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from .arithmetic import f_div
from .vtable import EUDVTable, VTProc
from .eudfunc import EUDFunc

f_epd = None

def _initepdcalc():
    global f_epd

    epdcalc_begin = Forward()
    epdcalc_end = Forward()
    vt = EUDVTable(2)
    addr, epd = vt.GetVariables()

    f_epd = EUDFunc(epdcalc_begin, epdcalc_end, vt, 1, 1)

    epdcalc_begin << Trigger(
        actions = [
            addr.AddNumber(0x100000000 - 0x58A364) # SubtractNumber don't underflow. So we use AddNumber to cause overflow.
        ]
    )

    ret_epd = f_div.call(addr, 4)[0]

    VTProc(ret_epd.GetVTable(), [
        ret_epd.QueueAssignTo(epd)
    ])

    epdcalc_end << Trigger()

_initepdcalc()
