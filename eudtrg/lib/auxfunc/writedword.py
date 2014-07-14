from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from eudtrg.lib.baselib import * #@UnusedWildImport


def f_dwwrite(targetplayer):
    if isinstance(targetplayer, EUDVariable):
        act = Forward()
        SeqCompute([
            (EPD(act + 16), SetTo, varname),
            (EPD(act + 20), SetTo, targetplayer)
        ])
        DoActions(act << SetMemory(0, SetTo, 0))

    else:
        act = Forward()
        SeqCompute([(EPD(act + 16), SetTo, varname)])
        DoActions(act << SetMemory(0, SetTo, targetplayer))