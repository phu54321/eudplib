from eudtrg import LICENSE  # @UnusedImport

from eudtrg.base import *  # @UnusedWildImport
from eudtrg.lib.baselib import *  # @UnusedWildImport

from .muldiv import f_div


@EUDFunc
def f_epd(addr):
    '''
    Convert address to EPD Player value. Use :func:`EPD` instead to convert
    Expr to EPD player value.

    :param addr: Address to convert.
    :returns: EPD player corresponding to given address.

    '''
    epd = EUDCreateVariables(1)
    DoActions(addr.AddNumber(-0x58A364))
    SetVariables(epd, f_div(addr, 4)[0])
    return epd
