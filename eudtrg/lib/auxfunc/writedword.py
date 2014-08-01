from eudtrg import LICENSE  # @UnusedImport

from eudtrg.base import *  # @UnusedWildImport
from eudtrg.lib.baselib import *  # @UnusedWildImport


def f_dwwrite(targetplayer, value):
    '''
    Writes value to specified address.

    :param targetplayer: EPD Player of address to write value.
    :param value: Value to write.
    '''
    if isinstance(value, EUDVariable):
        act = Forward()
        SeqCompute([
            (EPD(act + 16), SetTo, targetplayer),
            (EPD(act + 20), SetTo, value)
        ])
        DoActions(act << SetMemory(0, SetTo, 0))

    else:
        act = Forward()
        SeqCompute([(EPD(act + 16), SetTo, targetplayer)])
        DoActions(act << SetMemory(0, SetTo, value))
